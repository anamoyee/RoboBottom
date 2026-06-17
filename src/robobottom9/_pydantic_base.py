import pydantic as pd


class BM_Frozen(pd.BaseModel):
	model_config = pd.ConfigDict(
		extra="forbid",
		frozen=True,
	)
