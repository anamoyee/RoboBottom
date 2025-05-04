from common.bot import BOT
from prelude import *

from ..errors import UserGetsDetailsError
from ..models import GetByHashSet
from .model_profile import Profile, ProfileID


class UnableToEnsureProfileError(UserGetsDetailsError):
	"""User().ensure_profile() was called, but user has profiles, yet none are selected (bug or raw data alteration went wrong??)."""


class User(ZooBM):
	selected_profile_id: ProfileID | None = pd.Field(default=None)
	profiles: GetByHashSet[Profile] = pd.Field(default_factory=GetByHashSet)

	@property
	def selected_profile(self) -> Profile:
		"""Get the currently selected profile for this account as a mutable object to update (or just read).

		Raises RuntimeError if this account does not have any profiles selected (`.has_selected_profile()`).
		"""
		if not self.has_selected_profile():
			raise RuntimeError("This account does not have any profile selected. This happens when an account has no profiles or due to a bug.")
		return self.profiles[self.selected_profile_id]

	def has_selected_profile(self) -> bool:
		"""Whether or not this account has a valid selected profile. This is false only if this account has no profiles or has profiles but by eval/exec it was set to None or a bug in code is present."""
		return self.selected_profile_id is not None

	def select_profile(self, profile: ProfileID | Profile) -> None:
		"""Change the selected profile in this account to this profile by the Profile object or by the ProfileID enum variant.

		Raises ValueError if the user does not have this profile.
		"""
		if isinstance(profile, Profile):
			profile = profile.id

		if profile not in self.profiles:
			raise ValueError(f"Attempted to select a non-existent on this account profile: {profile!r}.")

		self.selected_profile_id = profile

	async def create_profile(
		self,
		*,
		owner: hikari.SnowflakeishOr[hikari.PartialUser],
		profile_id: ProfileID | None = None,
	) -> Profile:
		"""Create a new Profile with the given ProfileID and a default name, add it to the profiles set and return it."""
		owner_user = await BOT.rest.fetch_user(owner)

		if profile_id is None:
			profile_id = ProfileID.get_random(p.id for p in self.profiles)

		new_profile = Profile(id=profile_id, name=f"{owner_user.display_name}'s Zoo")

		self.profiles.add(new_profile)

		if not self.has_selected_profile():  # If that is the first profile of this account (or otherwise the current profile is not set), set it to it
			self.selected_profile_id = profile_id

		return new_profile

	async def ensure_profile(self, ctx: arc.GatewayContext) -> Profile:
		"""Ensure a profile is selected, if not - create one if there are no profiles, if everything went okay return that Profile.

		**!!! If there's at least 1 profile, but none is selected, raise UnableToEnsureProfileError with a bug message to the user**.

		## Usage:
		```
		with UserDB(ctx.author.id) as user:
			profile = await user.ensure_profile(ctx)
			# then use profile and not user.selected_profile
		```
		"""
		if not self.has_selected_profile():
			if self.profiles:
				raise UnableToEnsureProfileError("Huh... it looks like you have profiles, but dont have a profile selected..? Report this as a bug, or try re-selecting with /profiles")

			return await self.create_profile(owner=ctx.author)  # This also auto-selects the profile if none are selected already

		return self.selected_profile
