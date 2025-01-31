import pydantic as pd


class BM(pd.BaseModel):
	model_config = pd.ConfigDict(
		validate_assignment=True,
		validate_default=True,
		validate_return=True,
		arbitrary_types_allowed=True,
	)
