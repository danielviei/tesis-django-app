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
                        <button class="edit-button" data-comment-id="{comment.id}"><svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M12.5 5.00001L15 7.50001M10.8334 16.6667H17.5M4.16671 13.3333L3.33337 16.6667L6.66671 15.8333L16.3217 6.17835C16.6342 5.8658 16.8097 5.44195 16.8097 5.00001C16.8097 4.55807 16.6342 4.13423 16.3217 3.82168L16.1784 3.67835C15.8658 3.36589 15.442 3.19037 15 3.19037C14.5581 3.19037 14.1343 3.36589 13.8217 3.67835L4.16671 13.3333Z" stroke="black" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                        <button class="delete-button" data-comment-id="{comment.id}"><svg width="26" height="26" viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M8.24954 21.6667C7.76565 21.6667 7.3529 21.4962 7.01129 21.1553C6.6704 20.8144 6.49996 20.4017 6.49996 19.9171V6.49999H5.41663V5.41666H9.74996V4.58249H16.25V5.41666H20.5833V6.49999H19.5V19.9171C19.5 20.4154 19.3331 20.8314 18.9995 21.1651C18.6651 21.4995 18.2487 21.6667 17.7504 21.6667H8.24954ZM18.4166 6.49999H7.58329V19.9171C7.58329 20.1114 7.64576 20.271 7.77071 20.3959C7.89565 20.5209 8.05526 20.5833 8.24954 20.5833H17.7504C17.9165 20.5833 18.0692 20.514 18.2086 20.3753C18.3473 20.2359 18.4166 20.0832 18.4166 19.9171V6.49999ZM10.6253 18.4167H11.7086V8.66666H10.6253V18.4167ZM14.2913 18.4167H15.3746V8.66666H14.2913V18.4167Z" fill="black"/>
                            </svg>
                        </button>
                    </div>
                    <div id="delete-confirmation-{comment.id}" class="delete-confirmation" style="display: none;">
                        <p>¿Estás seguro de que quieres eliminar este comentario?</p>
                        <button class="delete-confirmation-button" data-comment-id="{comment.id}"><svg width="26" height="26" viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M8.24954 21.6667C7.76565 21.6667 7.3529 21.4962 7.01129 21.1553C6.6704 20.8144 6.49996 20.4017 6.49996 19.9171V6.49999H5.41663V5.41666H9.74996V4.58249H16.25V5.41666H20.5833V6.49999H19.5V19.9171C19.5 20.4154 19.3331 20.8314 18.9995 21.1651C18.6651 21.4995 18.2487 21.6667 17.7504 21.6667H8.24954ZM18.4166 6.49999H7.58329V19.9171C7.58329 20.1114 7.64576 20.271 7.77071 20.3959C7.89565 20.5209 8.05526 20.5833 8.24954 20.5833H17.7504C17.9165 20.5833 18.0692 20.514 18.2086 20.3753C18.3473 20.2359 18.4166 20.0832 18.4166 19.9171V6.49999ZM10.6253 18.4167H11.7086V8.66666H10.6253V18.4167ZM14.2913 18.4167H15.3746V8.66666H14.2913V18.4167Z" fill="black"/>
                            </svg>
                    </button>
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
