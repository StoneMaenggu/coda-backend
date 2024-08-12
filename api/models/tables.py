from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from api.db import Base

class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, index=True)
    phone_num = Column(String(20), unique=True, nullable=False)
    user_password = Column(String(20), nullable=False)
    user_name = Column(String(20), nullable=False)
    profile_path = Column(String(100))
    user_sex = Column(Boolean)
    user_birth = Column(DateTime)
    user_text_available = Column(Boolean, nullable=False)

    private_group = relationship("PrivateGroup", back_populates="user", cascade="delete")
    public_groups = relationship("UserHasPublicGroup", back_populates="user", cascade="delete")

class PrivateGroup(Base):
    __tablename__ = 'private_group'

    private_group_id = Column(Integer, primary_key=True, index=True)
    user_user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False, unique=True)
    private_group_header_path = Column(String(100))

    user = relationship("User", back_populates="private_group")
    posts = relationship("Posts", back_populates="private_group", cascade="delete")

class PublicGroup(Base):
    __tablename__ = 'public_group'

    public_group_id = Column(Integer, primary_key=True, index=True)
    master_user_id = Column(Integer, nullable=False)
    public_group_header_path = Column(String(100))
    public_group_name = Column(String(45))
    num_users = Column(Integer)

    user = relationship("UserHasPublicGroup", back_populates="public_group")
    posts = relationship("Posts", back_populates="public_group", cascade="delete")

class UserHasPublicGroup(Base):
    __tablename__ = 'user_has_public_group'

    user_public_id = Column(Integer, primary_key=True, index=True)
    user_user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    public_group_public_group_id = Column(Integer, ForeignKey('public_group.public_group_id', ondelete='CASCADE'), nullable=False)
    group_order = Column(Integer, nullable=False)

    user = relationship("User", back_populates="public_groups")
    public_group = relationship("PublicGroup", back_populates="user")

class Posts(Base):
    __tablename__ = 'posts'

    post_id = Column(Integer, primary_key=True, index=True)
    creation_date = Column(DateTime, nullable=False)
    creation_user_id = Column(Integer, nullable=False)
    public_group_public_group_id = Column(Integer, ForeignKey('public_group.public_group_id', ondelete='CASCADE'))
    private_group_private_group_id = Column(Integer, ForeignKey('private_group.private_group_id', ondelete='CASCADE'))
    post_header_path = Column(String(100), nullable=False)

    private_group = relationship("PrivateGroup", back_populates="posts")
    public_group = relationship("PublicGroup", back_populates="posts")
    reactions = relationship("Reaction", back_populates="post", cascade="delete")
    pictures = relationship("Picture", back_populates="post", cascade="delete")
    drawings = relationship("Drawing", back_populates="post", cascade="delete")

class Reaction(Base):
    __tablename__ = 'reaction'

    reaction_id = Column(Integer, primary_key=True, index=True)
    posts_post_id = Column(Integer, ForeignKey('posts.post_id', ondelete='CASCADE'), nullable=False)
    reaction_user_id = Column(Integer, nullable=False)
    emoji_id = Column(Integer, nullable=False)
    # emoji_emoji_id = Column(Integer, ForeignKey('emoji.emoji_id'), nullable=False)

    post = relationship("Posts", back_populates="reactions")
    # emoji = relationship("Emoji", back_populates="reactions")

class Picture(Base):
    __tablename__ = 'picture'

    picture_id = Column(Integer, primary_key=True, index=True)
    posts_post_id = Column(Integer, ForeignKey('posts.post_id', ondelete='CASCADE'), nullable=False)
    picture_path = Column(String(100), nullable=False)

    post = relationship("Posts", back_populates="pictures")

class Drawing(Base):
    __tablename__ = 'drawing'

    drawing_id = Column(Integer, primary_key=True, index=True)
    posts_post_id = Column(Integer, ForeignKey('posts.post_id', ondelete='CASCADE'), nullable=False)
    drawing_path = Column(String(100), nullable=False)
    drawing_order = Column(Integer, nullable=False)
    drawing_caption = Column(String(100), nullable=False)

    post = relationship("Posts", back_populates="drawings")

# class Emoji(Base):
#     __tablename__ = 'emoji'

#     emoji_id = Column(Integer, primary_key=True, index=True)
#     emoji_path = Column(String(100))

#     reactions = relationship("Reaction", back_populates="emoji", uselist=False)

class PoseToGloss(Base):
    __tablename__ = 'pose_to_gloss'

    pose_to_gloss_id = Column(Integer, primary_key=True, index=True)
    pose = Column(String(150), nullable=False)
    gloss = Column(String(150), nullable=False)

class GroupAccess(Base):
    __tablename__ = 'group_access'

    access_id = Column(Integer, primary_key=True, index=True)
    public_group_id = Column(Integer)
    access_key = Column(Integer, unique=True)
