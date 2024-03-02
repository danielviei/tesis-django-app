from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from project.models.publication import Publication
from project.models.comment_serializers import CommentSerializer
from project.models.comment import Comment


class EditCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        if request.user != comment.author_id:
            return Response(
                {"error": "You do not have permission to edit this comment."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        if request.user != comment.author_id:
            return Response(
                {"error": "You do not have permission to delete this comment."},
                status=status.HTTP_403_FORBIDDEN,
            )
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            publication = Publication.objects.get(pk=pk)
            serializer.save(author_id=request.user, publication_id=publication)
            comments_html = self.get_context_data(pk, request.user)["comments_html"]
            return Response({"comments_html": comments_html})
        else:
            return Response(serializer.errors, status=400)

    def get_context_data(self, pk, user):
        publication = Publication.objects.get(pk=pk)
        comments = publication.comments.all()

        comments_html = '<ul class="list-none space-y-4">'
        for comment in comments:
            if comment.author_id == user:
                comments_html += f"""
                <li id="comment-{comment.id}" class="p-4 rounded-md bg-gray-100">
                    <div class="flex items-center">
                        <img src="{comment.author_id.img.url}" alt="{comment.author_id.email} profile picture" class="w-10 h-10 rounded-full mr-4">
                        <div>
                            <div class="flex justify-around">
                                <h4 class="text-md font-bold text-gray-800">{comment.author_id.email}</h4>
                                <div>
                        <button class="edit-button" data-comment-id="{comment.id}">editar</button>
                        <button class="delete-button" data-comment-id="{comment.id}">eliminar</button>
                    </div>
                    <div id="delete-confirmation-{comment.id}" class="delete-confirmation" style="display: none;">
                        <p>¿Estás seguro de que quieres eliminar este comentario?</p>
                        <button class="delete-confirmation-button" data-comment-id="{comment.id}">Eliminar</button>
                    </div>
                            </div>
                            <p id="comment-{comment.id}-content" class="text-gray-600">{comment.content}</p>
                        </div>
                    </div>
                    <form id="edit-form-{comment.id}" class="edit-form p-2" data-comment-id="{comment.id}" style="display: none;">
                        <textarea>{comment.content}</textarea>
                        <button type="submit">Guardar</button>
                    </form>
                """
            else:
                comments_html += f"""
                <li id="comment-{comment.id}" class="p-4 rounded-md bg-gray-100">
                    <div class="flex items-center">
                        <img src="{comment.author_id.img.url}" alt="{comment.author_id.email} profile picture" class="w-10 h-10 rounded-full mr-4">
                        <div>
                            <div class="flex justify-around">
                                <h4 class="text-md font-bold text-gray-800">{comment.author_id.email}</h4>
                            </div>
                            <p id="comment-{comment.id}-content" class="text-gray-600">{comment.content}</p>
                        </div>
                    </div>
                """
            comments_html += "</li>"
        comments_html += "</ul>"

        return {"comments_html": comments_html}
