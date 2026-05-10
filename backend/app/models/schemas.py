from pydantic import BaseModel, ConfigDict, Field


class AnalyseRequest(BaseModel):
    model_config = ConfigDict(strict=True)
    hashPrefix: str = Field(min_length=5, max_length=5, pattern=r"^[A-F0-9]{5}$")


class AnalyseResponse(BaseModel):
    model_config = ConfigDict(strict=True)
    isBreached: bool
    breachCount: int


class AdviseRequest(BaseModel):
    model_config = ConfigDict(strict=True)
    strengthScore: int
    zxcvbnScore: int
    crackTime: str
    warning: str
    suggestions: list[str]
    hasDictionaryMatch: bool
    hasL33tSub: bool
    hasKeyboardPattern: bool
    hasDatePattern: bool
    hasRepeat: bool
    hasSequence: bool
    rulesPassed: int
    rulesTotal: int
    isBreached: bool
    breachCount: int
