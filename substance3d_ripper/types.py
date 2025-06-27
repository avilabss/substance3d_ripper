from pydantic import BaseModel, Field


class UserInfo(BaseModel):
    account_type: str
    address: str
    utcOffset: str
    preferred_languages: list[str]
    displayName: str
    last_name: str
    token_type: str
    userId: str
    authId: str
    tags: list[str]
    access_token: str
    emailVerified: str
    phoneNumber: str | None
    countryCode: str
    name: str
    mrktPerm: str
    mrktPermEmail: str
    first_name: str
    expires_in: str
    email: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls.model_validate(data)


class AssetThumbnail(BaseModel):
    id: str
    url: str
    tags: list[str]
    typename: str = Field(alias="__typename")


class AssetAttachment(BaseModel):
    id: str
    tags: list[str]
    label: str
    kind: str | None = None
    url: str | None = None
    typename: str = Field(alias="__typename")


class AssetItem(BaseModel):
    id: str
    title: str
    tags: list[str]
    status: str
    categories: list[str]
    cost: int
    new: bool
    free: bool
    licenses: list[str]
    downloadsRecentlyUpdated: bool
    thumbnail: AssetThumbnail
    createdAt: str
    typename: str = Field(alias="__typename")
    attachments: list[AssetAttachment]


class Asset(BaseModel):
    total: int
    hasMore: bool
    items: list[AssetItem]
    typename: str = Field(alias="__typename")


class Collection(BaseModel):
    id: str
    title: str
    imageUrl: str
    assets: Asset

    @classmethod
    def from_dict(cls, data: dict):
        return cls.model_validate(data)
