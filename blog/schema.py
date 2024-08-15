import graphene
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from .models import Author, Post, Comment

# GraphQL Types
class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email")

class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = ("id", "name", "email", "bio")

class PostType(DjangoObjectType):
    comments = graphene.List(lambda: CommentType)  # Add comments field to PostType
    author = graphene.Field(UserType)  # Expose the User model as author in the schema

    class Meta:
        model = Post
        fields = ("id", "title", "content", "created_at", "updated_at", "author", "last_updated")

    def resolve_comments(self, info):
        return self.comments.all()  # Resolve comments related to this post

    def resolve_author(self, info):  # Custom resolver for the author field
        return self.author

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ("id", "content", "created_at", "post")

# Queries
class Query(graphene.ObjectType):
    all_authors = graphene.List(AuthorType)
    all_posts = graphene.List(
        PostType,
        author_id=graphene.Int(),
        title_contains=graphene.String(),
        content_contains=graphene.String(),
        skip=graphene.Int(),
        limit=graphene.Int()
    )
    
    post_by_id = graphene.Field(PostType, id=graphene.Int(required=True))
    comments_by_post = graphene.List(CommentType, post_id=graphene.Int(required=True))

    def resolve_all_authors(self, info):
        return Author.objects.all()

    def resolve_all_posts(self, info, author_id=None, title_contains=None, content_contains=None, skip=0, limit=10):
        try:
            posts = Post.objects.all()
            if author_id:
                posts = posts.filter(author_id=author_id)
            if title_contains:
                posts = posts.filter(title__icontains=title_contains)
            if content_contains:
                posts = posts.filter(content__icontains=content_contains)
            return posts[skip: skip + limit]  # Apply pagination
        except Exception as e:
            raise Exception(f"Error fetching posts: {str(e)}")

    def resolve_post_by_id(self, info, id):
        try:
            return Post.objects.get(pk=id)
        except Post.DoesNotExist:
            raise Exception("Post not found")
        except Exception as e:
            raise Exception(f"Error fetching post: {str(e)}")

    def resolve_comments_by_post(self, info, post_id):
        try:
            return Comment.objects.filter(post_id=post_id)
        except Exception as e:
            raise Exception(f"Error fetching comments: {str(e)}")

# Mutations
class CreateAuthor(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        bio = graphene.String()

    author = graphene.Field(AuthorType)

    def mutate(self, info, name, email, bio=None):
        try:
            author = Author(name=name, email=email, bio=bio)
            author.save()
            return CreateAuthor(author=author)
        except Exception as e:
            raise Exception(f"Error creating author: {str(e)}")

class UpdateAuthor(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        email = graphene.String()
        bio = graphene.String()

    author = graphene.Field(AuthorType)

    def mutate(self, info, id, name=None, email=None, bio=None):
        try:
            author = Author.objects.get(pk=id)
            if name:
                author.name = name
            if email:
                author.email = email
            if bio:
                author.bio = bio
            author.save()
            return UpdateAuthor(author=author)
        except Author.DoesNotExist:
            raise Exception("Author not found")
        except Exception as e:
            raise Exception(f"Error updating author: {str(e)}")

class DeleteAuthor(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            author = Author.objects.get(pk=id)
            author.delete()
            return DeleteAuthor(success=True)
        except Author.DoesNotExist:
            raise Exception("Author not found")
        except Exception as e:
            raise Exception(f"Error deleting author: {str(e)}")

class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)

    post = graphene.Field(PostType)

    def mutate(self, info, title, content):
        user = info.context.user
        print(f"User: {user}")
        if user.is_anonymous:
            raise Exception("You must be logged in to create a post.")
        post = Post(title=title, content=content, author=user)
        post.save()
        return CreatePost(post=post)

class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        content = graphene.String()

    post = graphene.Field(PostType)

    def mutate(self, info, id, title=None, content=None):
        user = info.context.user
        post = Post.objects.get(pk=id)
        if post.author != user:
            raise Exception("You can only update your own posts.")
        if title:
            post.title = title
        if content:
            post.content = content
        post.save()
        return UpdatePost(post=post)

class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            post = Post.objects.get(pk=id)
            post.delete()
            return DeletePost(success=True)
        except Post.DoesNotExist:
            raise Exception("Post not found")
        except Exception as e:
            raise Exception(f"Error deleting post: {str(e)}")

class CreateComment(graphene.Mutation):
    class Arguments:
        content = graphene.String(required=True)
        post_id = graphene.Int(required=True)

    comment = graphene.Field(CommentType)

    def mutate(self, info, content, post_id):
        try:
            post = Post.objects.get(pk=post_id)
            comment = Comment(content=content, post=post)
            comment.save()
            return CreateComment(comment=comment)
        except Post.DoesNotExist:
            raise Exception("Post not found")
        except Exception as e:
            raise Exception(f"Error creating comment: {str(e)}")

class UpdateComment(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        content = graphene.String()

    comment = graphene.Field(CommentType)

    def mutate(self, info, id, content=None):
        try:
            comment = Comment.objects.get(pk=id)
            if content:
                comment.content = content
            comment.save()
            return UpdateComment(comment=comment)
        except Comment.DoesNotExist:
            raise Exception("Comment not found")
        except Exception as e:
            raise Exception(f"Error updating comment: {str(e)}")

class DeleteComment(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            comment = Comment.objects.get(pk=id)
            comment.delete()
            return DeleteComment(success=True)
        except Comment.DoesNotExist:
            raise Exception("Comment not found")
        except Exception as e:
            raise Exception(f"Error deleting comment: {str(e)}")

# JWT Authentication Mutation
class ObtainTokenMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.String()
    refresh_token = graphene.String()

    @classmethod
    def mutate(cls, root, info, username, password):
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return ObtainTokenMutation(
                token=str(refresh.access_token),
                refresh_token=str(refresh),
            )
        else:
            raise Exception("Invalid credentials")

# Register mutations
class Mutation(graphene.ObjectType):
    create_author = CreateAuthor.Field()
    update_author = UpdateAuthor.Field()
    delete_author = DeleteAuthor.Field()
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
    create_comment = CreateComment.Field()
    update_comment = UpdateComment.Field()
    delete_comment = DeleteComment.Field()
    token_auth = ObtainTokenMutation.Field()  # Add JWT Authentication Mutation

schema = graphene.Schema(query=Query, mutation=Mutation)
