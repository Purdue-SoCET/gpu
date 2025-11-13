@dataclass
class IntUnitConfig:
    alu_count: int
    mul_count: int
    div_count: int
    
    alu_latency: int
    mul_latency: int
    div_latency: int

    def __post_init__(self):
        raise TypeError(f"{self.__class__.__name__} cannot be instantiated directly. Use class methods like get_default_config()")

    @classmethod
    def get_default_config(cls) -> IntUnitConfig:
        return cls(
            alu_count=1,
            mul_count=1,
            div_count=1,
            alu_latency=1,
            mul_latency=2,
            div_latency=17
        )

@dataclass
class FpUnitConfig:
    add_sub_count: int
    mul_count: int
    div_count: int
    sqrt_count: int
    
    add_sub_latency: int
    mul_latency: int
    div_latency: int
    sqrt_latency: int

    def __post_init__(self):
        raise TypeError(f"{self.__class__.__name__} cannot be instantiated directly. Use class methods like get_default_config()")

    @classmethod
    def get_default_config(cls) -> FpUnitConfig:
        return cls(
            add_sub_count=1,
            mul_count=1,
            div_count=1,
            sqrt_count=1,
            add_sub_latency=1,
            mul_latency=4,
            div_latency=24,
            sqrt_latency=20
        )

@dataclass
class SpecialUnitConfig:
    trig_count: int
    inv_sqrt_count: int

    trig_latency: int
    inv_sqrt_latency: int

    def __post_init__(self):
        raise TypeError(f"{self.__class__.__name__} cannot be instantiated directly. Use class methods like get_default_config()")

    @classmethod
    def get_default_config(cls) -> SpecialUnitConfig:
        return cls(
            trig_count=1,
            inv_sqrt_count=1,
            trig_latency=16,
            inv_sqrt_latency=12
        )

@dataclass
class FunctionalUnitConfig:
    int_unit_count: int
    fp_unit_count: int
    special_unit_count: int

    int_config: IntUnitConfig
    fp_config: FpUnitConfig
    special_config: SpecialUnitConfig

    def __post_init__(self):
        raise TypeError(f"{self.__class__.__name__} cannot be instantiated directly. Use class methods like get_default_config()")

    @classmethod
    def get_default_config(cls) -> FunctionalUnitConfig:
        return cls(
            int_unit_count=1,
            fp_unit_count=1,
            special_unit_count=1,
            int_config=IntUnitConfig().get_default_config(),
            fp_config=FpUnitConfig().get_default_config(),
            special_config=SpecialUnitConfig().get_default_config()
        )

@dataclass
class FULatchData():
    def __init__(self, instr: Instr, pc: Bits, thread_id: Bits, warp_id: Bits, a: list[Bits], b: list[Bits]):
        self.instr = instr
        self.pc = pc
        self.thread_id = thread_id
        self.warp_id = warp_id
        self.a = [Bits(length=32, bin=0)] * 32
        self.b = [Bits(length=32, bin=0)] * 32
        for i in range(32):
            self.a[i] = Bits(length=32, bin=a[i].bin)
            self.b[i] = Bits(length=32, bin=b[i].bin)

    @classmethod
    def NOP(cls) -> FULatchData:
        return cls(instr=None, pc=Bits(length=32, bin=0), thread_id=Bits(length=8, bin=0), warp_id=Bits(length=8, bin=0), a=[Bits(length=32, bin=0)] * 32, b=[Bits(length=32, bin=0)] * 32)
    
class FunctionalUnitPipeline(CompactQueue):
    def __init__(self, latency: int, ):
        super().__init__(length=1, type_=FULatchData)

class ArithmeticFunctionalUnit(ABC):
    def __init__(self, subunits: list[FunctionalSubUnit], num: int):
        self.name = f"{self.__class__.__name__}_{num}"

        # Convert list of subunits to dict using the names of the subunits as keys
        self.subunits = {subunit.name: subunit for subunit in subunits}        

    def compute(self, instr: Instruction):
        for subunit in self.subunits.values():
            subunit.compute(instr)

    def tick(self, is_ex_latch: LatchIF, ex_wb_latch: LatchIF) -> List[Instruction]:
        out_data = {}
        for subunit in self.subunits.values():
            out_data[subunit.name] = subunit.tick(is_ex_latch, ex_wb_latch)

        return out_data

class FunctionalSubUnit(ABC):
    def __init__(self, latency: int, type_: type, num: int):
        self.name = f"{self.__class__.__name__}_{num}"
        self.latency = latency
        self.ready_out = True

        if type_ not in [int, float]:
            raise ValueError(f"Unsupported type '{type_}' for FunctionalSubUnit. Must be {int} or {float}.")

        self.type_ = type_

        # the way stages are connected in the SM class, we need (latency - 2) latches
        self.pipeline = FunctionalUnitPipeline(latency=latency-1)
    
    @abstractmethod
    def compute(self, instr: Instruction):
        pass

    def tick(self, is_ex_latch: LatchIF, ex_wb_latch: LatchIF) -> Instruction:
        # Shift latches
        in_data = is_ex_latch.snoop()
        self.ready_out = True

        if ex_wb_latch.ready_for_push():
            out_data = self.pipeline.advance(in_data)
            is_ex_latch.pop()
        else:
            out_data = None
            self.pipeline.compact(in_data)
            if not self.pipeline.is_full:
                is_ex_latch.pop()
            else: 
                self.ready_out = False
        
        return out_data # return data to the Exectute stage so that all results can be collected and sent to WB stage together

class IntUnit(ArithmeticFunctionalUnit):
    def __init__(self, config: IntUnitConfig):
        subunits = []
        for i in range(config.alu_count):
            subunits.append(Alu(latency=config.alu_latency, type_=int, num=i))
        for i in range(config.mul_count):
            subunits.append(Mul(latency=config.mul_latency, type_=int, num=i))
        for i in range(config.div_count):
            subunits.append(Div(latency=config.div_latency, type_=int, num=i))

        super().__init__(subunits=subunits)

class FpUnit(ArithmeticFunctionalUnit):
    def __init__(self, config: FpUnitConfig):
        subunits = []
        for i in range(config.add_sub_count):
            subunits.append(AddSub(latency=config.add_sub_latency, type_=float, num=i))
        for i in range(config.mul_count):
            subunits.append(Mul(latency=config.mul_latency, type_=float, num=i))
        for i in range(config.div_count):
            subunits.append(Div(latency=config.div_latency, type_=float, num=i))
        for i in range(config.sqrt_count):
            subunits.append(Sqrt(latency=config.sqrt_latency, type_=float, num=i))

        super().__init__(subunits=subunits)

class SpecialUnit(ArithmeticFunctionalUnit):
    def __init__(self, config: SpecialUnitConfig):
        subunits = []
        for i in range(config.trig_count):
            subunits.append(Trig(latency=config.trig_latency, type_=float, num=i))
        for i in range(config.inv_sqrt_count):
            subunits.append(InvSqrt(latency=config.inv_sqrt_latency, type_=float, num=i))

        super().__init__(subunits=subunits)

class Alu(FunctionalSubUnit):
    def __init__(self, latency: int, type_: type = int):
        if self.type_ != int:
            raise ValueError("ALU only supports integer operations.")

        super().__init__(latency=latency, type_=type_)

    def compute():

class ExecuteStage(Stage):
    def __init__(self, config: FunctionalUnitConfig):
        super().__init__()

        functional_units_list = []
        for i in range(config.int_unit_count):
            functional_units_list.append(IntUnit(config=config.int_config, num=i))
        for i in range(config.fp_unit_count):
            functional_units_list.append(FpUnit(config=fp_unit_config, num=i))
        for i in range(config.special_unit_count):
            functional_units_list.append(SpecialUnit(config=special_unit_config, num=i))

        self.functional_units = {fu.name: fu for fu in functional_units_list}

    def compute(self) -> None:
        if self.forward_if_read and self.forward_if_read.wait:
            print(f"[{self.name}] Stalled due to wait from next stage.")
            return None
        if self.behind_latch and not self.behind_latch.valid:
            return None
        
        input_to_stage: FULatchData = self.behind_latch.pop()
        
        # Dispatch to functional units
        for fu in self.functional_units:
            fu.compute(input_to_stage.instr)

    def tick(self) -> None:
        # Tick all functional units
        out_data = {}
        for fu in self.functional_units:
            out_data[fu.name] = fu.tick(is_ex_latch=self.behind_latch, ex_wb_latch=self.ahead_latch)

        if self.ahead_latch.ready_for_push():
            

        # Collect results and send to ahead latch
        # (Implementation of result collection and sending to ahead latch goes here)

    @classmethod
    def create_default_execute_pipeline_stage(cls) -> Stage:
        # execute stage
        functional_unit_config = FunctionalUnitConfig.get_default_config()

        ex_stage = ExecuteStage(config=functional_unit_config)

        ex_stage.name = "Execute"
        ex_stage.behind_latch = LatchIF(name="IS_EX_Latch")
        ex_stage.ahead_latch = LatchIF(name="EX_WB_Latch")

        return ex_stage