from django.test import TestCase
from .models import Author, Post, Comment
from graphene_django.utils.testing import GraphQLTestCase
from blog_api.schema import schema

# Model Tests
class AuthorModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Jonathan Moore", email="john@example.com", bio="A test author.")

    def test_author_creation(self):
        self.assertEqual(self.author.name, "Jonathan Moore")
        self.assertEqual(self.author.email, "john@example.com")
        self.assertEqual(self.author.bio, "A test author.")

class PostModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Jonathan Moore", email="john@example.com", bio="A test author.")
        self.post = Post.objects.create(title="Test Post", content="Test Content", author=self.author)

    def test_post_creation(self):
        self.assertEqual(self.post.title, "Test Post")
        self.assertEqual(self.post.content, "Test Content")
        self.assertEqual(self.post.author.name, "Jonathan Moore")

class CommentModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Jonathan Moore", email="john@example.com", bio="A test author.")
        self.post = Post.objects.create(title="Test Post", content="Test Content", author=self.author)
        self.comment = Comment.objects.create(content="Test Comment", post=self.post)

    def test_comment_creation(self):
        self.assertEqual(self.comment.content, "Test Comment")
        self.assertEqual(self.comment.post.title, "Test Post")


# GraphQL Query Tests
class BlogQueryTest(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    GRAPHQL_URL = '/graphql/'  # Ensure the correct GraphQL URL is used

    def setUp(self):
        self.author = Author.objects.create(name="Jonathan Moore", email="john@example.com", bio="A test author.")
        self.post = Post.objects.create(title="Test Post", content="Test Content", author=self.author)
        self.comment = Comment.objects.create(content="Test Comment", post=self.post)

    def test_all_posts_query(self):
        response = self.query(
            '''
            query {
                allPosts {
                    id
                    title
                    content
                    author {
                        name
                    }
                }
            }
            '''
        )
        # Check the status code and response content
        print(response.status_code)
        print(response.content)
        content = response.json()
        self.assertResponseNoErrors(response)
        self.assertEqual(len(content['data']['allPosts']), 1)
        self.assertEqual(content['data']['allPosts'][0]['title'], "Test Post")

    def test_post_by_id_query(self):
        response = self.query(
            '''
            query {
                postById(id: 1) {
                    title
                    content
                    author {
                        name
                    }
                }
            }
            '''
        )
        print(response.status_code)
        print(response.content)
        content = response.json()
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['postById']['title'], "Test Post")

    def test_comments_by_post_query(self):
        response = self.query(
            '''
            query {
                commentsByPost(postId: 1) {
                    content
                }
            }
            '''
        )
        print(response.status_code)
        print(response.content)
        content = response.json()
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['commentsByPost'][0]['content'], "Test Comment")


# GraphQL Mutation Tests
class BlogMutationTest(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    GRAPHQL_URL = '/graphql/'  # Ensure the correct GraphQL URL is used

    def setUp(self):
        self.author = Author.objects.create(name="Jonathan Moore", email="john@example.com", bio="A test author.")
        self.post = Post.objects.create(title="Test Post", content="Test Content", author=self.author)

    def test_create_post_mutation(self):
        response = self.query(
            '''
            mutation {
                createPost(title: "New Post", content: "New Content", authorId: 1) {
                    post {
                        title
                        content
                    }
                }
            }
            '''
        )
        print(response.status_code)
        print(response.content)
        content = response.json()
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['createPost']['post']['title'], "New Post")

    def test_update_post_mutation(self):
        response = self.query(
            '''
            mutation {
                updatePost(id: 1, title: "Updated Post") {
                    post {
                        title
                    }
                }
            }
            '''
        )
        print(response.status_code)
        print(response.content)
        content = response.json()
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['updatePost']['post']['title'], "Updated Post")

    def test_delete_post_mutation(self):
        response = self.query(
            '''
            mutation {
                deletePost(id: 1) {
                    success
                }
            }
            '''
        )
        print(response.status_code)
        print(response.content)
        content = response.json()
        self.assertResponseNoErrors(response)
        self.assertTrue(content['data']['deletePost']['success'])
