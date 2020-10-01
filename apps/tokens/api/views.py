from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import (
    viewsets,
    serializers,
    status
)
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
)
from rest_framework.views import APIView
from apps.tokens.models import *
from apps.tokens.api.serializers import *

# class TokenView(viewsets.ModelViewSet):
#   queryset = Token.objects.all()
#   serializer_class = TokenSerializer
#   # lookup_field='id'

#   # for custom handling of http method 'post' override the
#   # create() function and write your custom logic
#   # you can find more from 'http://cdrf.co'

#   def create(self, request, *args, **kwargs):
#     serializer = self.get_serializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     result = self.perform_create(serializer)
#     response = serializer.data

#     return Response(
#         data={
#             'status': True,
#             'message': "Token stored successfully",
#             'data': response
#         },
#         status=status.HTTP_201_CREATED
#     )


#   def list(self, request, *args, **kwargs):
#     try:
#       queryset = self.filter_queryset(self.get_queryset())

#       # PAGINATION PURPOSE
#       # We are setting default number of items per page = 40
#       # By default we set starting index 0 and ending index 39 (index=9 means serially 10th item) [see python data slicing mechanism to know more ]
#       page_number = self.request.query_params.get('page')
#       number_of_items_per_page = self.request.query_params.get(
#           'items')
#       # Although user can request for number_of_items_per_page via the url, we set it default 40
#       items_per_page = 40
#       start = 0
#       end = items_per_page

#       if(page_number != None and number_of_items_per_page != None):
#           start = int(number_of_items_per_page) * \
#               int(page_number) - int(number_of_items_per_page)
#           end = int(number_of_items_per_page) * int(page_number)

#       elif(page_number != None and number_of_items_per_page == None):
#           start = items_per_page * int(page_number) - items_per_page
#           end = items_per_page * int(page_number)

#       elif(page_number == None and number_of_items_per_page != None):
#           # Since user didn't give page_number, we assume he wants the first page (i,e page_number = 1)
#           start = int(number_of_items_per_page) * 1 - \
#               int(number_of_items_per_page)
#           end = int(number_of_items_per_page) * 1

#       if(page_number == None):
#           page_number = 1

#       queryset = queryset[start:end]

#       serializer = self.get_serializer(queryset, many=True)
#       return Response(
#           data={
#               'status': True,
#               'page_number': page_number,
#               'total': len(serializer.data),
#               'message': "All tokens",
#               'data': serializer.data
#           },
#           status=status.HTTP_200_OK
#       )

#     except Exception as ex:
#       return Response(
#         data={
#           'status': False,
#           'message': "Something wrong"
#         },
#         status=status.HTTP_404_NOT_FOUND
#       )


#   def retrieve(self, request, *args, **kwargs):
#     try:
#       instance = self.get_object()
#       #above line will create an instance with the provided 'id' in the url. Since, we
#       #setup 'lookup_field=id', it will search the 'id' column with the provided id.

#       serializer = self.get_serializer(instance) # serializing the queryied data
#       return Response(
#         data={
#           'status': True,
#           'message': "Tokens information",
#           'data': serializer.data
#         },
#         status=status.HTTP_200_OK
#       )

#     except Exception as ex:
#       return Response(
#         data={
#           'status': False,
#           'message': "Token not found"
#         },
#         status=status.HTTP_404_NOT_FOUND
#       )


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # lookup_field='id'

    # for custom handling of http method 'post' override the
    # create() function and write your custom logic
    # you can find more from 'http://cdrf.co'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.perform_create(serializer)
        response = serializer.data

        return Response(
            data={
                'status': True,
                'message': "User created",
                'data': response
            },
            status=status.HTTP_201_CREATED
        )

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            # PAGINATION PURPOSE
            # We are setting default number of items per page = 40
            # By default we set starting index 0 and ending index 39 (index=9 means serially 10th item) [see python data slicing mechanism to know more ]
            page_number = self.request.query_params.get('page')
            number_of_items_per_page = self.request.query_params.get(
                'items')
            # Although user can request for number_of_items_per_page via the url, we set it default 40
            items_per_page = 40
            start = 0
            end = items_per_page

            if(page_number != None and number_of_items_per_page != None):
                start = int(number_of_items_per_page) * \
                    int(page_number) - int(number_of_items_per_page)
                end = int(number_of_items_per_page) * int(page_number)

            elif(page_number != None and number_of_items_per_page == None):
                start = items_per_page * int(page_number) - items_per_page
                end = items_per_page * int(page_number)

            elif(page_number == None and number_of_items_per_page != None):
                # Since user didn't give page_number, we assume he wants the first page (i,e page_number = 1)
                start = int(number_of_items_per_page) * 1 - \
                    int(number_of_items_per_page)
                end = int(number_of_items_per_page) * 1

            if(page_number == None):
                page_number = 1

            queryset = queryset[start:end]

            serializer = self.get_serializer(queryset, many=True)
            return Response(
                data={
                    'status': True,
                    'page_number': page_number,
                    'total': len(serializer.data),
                    'message': "All tokens",
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception as ex:
            return Response(
                data={
                    'status': False,
                    'message': "Something wrong"
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # above line will create an instance with the provided 'id' in the url. Since, we
            # setup 'lookup_field=id', it will search the 'id' column with the provided id.

            # serializing the queryied data
            serializer = self.get_serializer(instance)
            return Response(
                data={
                    'status': True,
                    'message': "Tokens information",
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception as ex:
            return Response(
                data={
                    'status': False,
                    'message': "Token not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )


class ExamView(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    # lookup_field='id'

    # for custom handling of http method 'post' override the
    # create() function and write your custom logic
    # you can find more from 'http://cdrf.co'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.perform_create(serializer)
        response = serializer.data

        return Response(
            data={
                'status': True,
                'message': "User created",
                'data': response
            },
            status=status.HTTP_201_CREATED
        )

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            # PAGINATION PURPOSE
            # We are setting default number of items per page = 40
            # By default we set starting index 0 and ending index 39 (index=9 means serially 10th item) [see python data slicing mechanism to know more ]
            page_number = self.request.query_params.get('page')
            number_of_items_per_page = self.request.query_params.get(
                'items')
            # Although user can request for number_of_items_per_page via the url, we set it default 40
            items_per_page = 40
            start = 0
            end = items_per_page

            if(page_number != None and number_of_items_per_page != None):
                start = int(number_of_items_per_page) * \
                    int(page_number) - int(number_of_items_per_page)
                end = int(number_of_items_per_page) * int(page_number)

            elif(page_number != None and number_of_items_per_page == None):
                start = items_per_page * int(page_number) - items_per_page
                end = items_per_page * int(page_number)

            elif(page_number == None and number_of_items_per_page != None):
                # Since user didn't give page_number, we assume he wants the first page (i,e page_number = 1)
                start = int(number_of_items_per_page) * 1 - \
                    int(number_of_items_per_page)
                end = int(number_of_items_per_page) * 1

            if(page_number == None):
                page_number = 1

            queryset = queryset[start:end]

            serializer = self.get_serializer(queryset, many=True)
            return Response(
                data={
                    'status': True,
                    'page_number': page_number,
                    'total': len(serializer.data),
                    'message': "All exams",
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception as ex:
            return Response(
                data={
                    'status': False,
                    'message': "Something wrong"
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # above line will create an instance with the provided 'id' in the url. Since, we
            # setup 'lookup_field=id', it will search the 'id' column with the provided id.

            # serializing the queryied data
            serializer = self.get_serializer(instance)
            return Response(
                data={
                    'status': True,
                    'message': "Exam information",
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception as ex:
            return Response(
                data={
                    'status': False,
                    'message': "Exam not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )


class QuestionView(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    # lookup_field='id'

    # for custom handling of http method 'post' override the
    # create() function and write your custom logic
    # you can find more from 'http://cdrf.co'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.perform_create(serializer)
        response = serializer.data

        return Response(
            data={
                'status': True,
                'message': "Question created",
                'data': response
            },
            status=status.HTTP_201_CREATED
        )

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            # PAGINATION PURPOSE
            # We are setting default number of items per page = 40
            # By default we set starting index 0 and ending index 39 (index=9 means serially 10th item) [see python data slicing mechanism to know more ]
            page_number = self.request.query_params.get('page')
            number_of_items_per_page = self.request.query_params.get(
                'items')
            # Although user can request for number_of_items_per_page via the url, we set it default 40
            items_per_page = 40
            start = 0
            end = items_per_page

            if(page_number != None and number_of_items_per_page != None):
                start = int(number_of_items_per_page) * \
                    int(page_number) - int(number_of_items_per_page)
                end = int(number_of_items_per_page) * int(page_number)

            elif(page_number != None and number_of_items_per_page == None):
                start = items_per_page * int(page_number) - items_per_page
                end = items_per_page * int(page_number)

            elif(page_number == None and number_of_items_per_page != None):
                # Since user didn't give page_number, we assume he wants the first page (i,e page_number = 1)
                start = int(number_of_items_per_page) * 1 - \
                    int(number_of_items_per_page)
                end = int(number_of_items_per_page) * 1

            if(page_number == None):
                page_number = 1

            queryset = queryset[start:end]

            serializer = self.get_serializer(queryset, many=True)
            return Response(
                data={
                    'status': True,
                    'page_number': page_number,
                    'total': len(serializer.data),
                    'message': "All exams",
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception as ex:
            return Response(
                data={
                    'status': False,
                    'message': "Something wrong"
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # above line will create an instance with the provided 'id' in the url. Since, we
            # setup 'lookup_field=id', it will search the 'id' column with the provided id.

            # serializing the queryied data
            serializer = self.get_serializer(instance)
            return Response(
                data={
                    'status': True,
                    'message': "Exam information",
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception as ex:
            return Response(
                data={
                    'status': False,
                    'message': "Exam not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )


class UserExamView(viewsets.ModelViewSet):
    queryset = UserExam.objects.all()
    serializer_class = UserExamSerializer
    # lookup_field='id'

    # for custom handling of http method 'post' override the
    # create() function and write your custom logic
    # you can find more from 'http://cdrf.co'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.perform_create(serializer)
        response = serializer.data

        return Response(
            data={
                'status': True,
                'message': "User-exam created",
                'data': response
            },
            status=status.HTTP_201_CREATED
        )

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            # PAGINATION PURPOSE
            # We are setting default number of items per page = 40
            # By default we set starting index 0 and ending index 39 (index=9 means serially 10th item) [see python data slicing mechanism to know more ]
            page_number = self.request.query_params.get('page')
            number_of_items_per_page = self.request.query_params.get(
                'items')
            # Although user can request for number_of_items_per_page via the url, we set it default 40
            items_per_page = 40
            start = 0
            end = items_per_page

            if(page_number != None and number_of_items_per_page != None):
                start = int(number_of_items_per_page) * \
                    int(page_number) - int(number_of_items_per_page)
                end = int(number_of_items_per_page) * int(page_number)

            elif(page_number != None and number_of_items_per_page == None):
                start = items_per_page * int(page_number) - items_per_page
                end = items_per_page * int(page_number)

            elif(page_number == None and number_of_items_per_page != None):
                # Since user didn't give page_number, we assume he wants the first page (i,e page_number = 1)
                start = int(number_of_items_per_page) * 1 - \
                    int(number_of_items_per_page)
                end = int(number_of_items_per_page) * 1

            if(page_number == None):
                page_number = 1

            queryset = queryset[start:end]

            serializer = self.get_serializer(queryset, many=True)
            return Response(
                data={
                    'status': True,
                    'page_number': page_number,
                    'total': len(serializer.data),
                    'message': "All exams",
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception as ex:
            return Response(
                data={
                    'status': False,
                    'message': "Something wrong"
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # above line will create an instance with the provided 'id' in the url. Since, we
            # setup 'lookup_field=id', it will search the 'id' column with the provided id.

            # serializing the queryied data
            serializer = self.get_serializer(instance)
            return Response(
                data={
                    'status': True,
                    'message': "Exam information",
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception as ex:
            return Response(
                data={
                    'status': False,
                    'message': "Exam not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )


class UserExamDetailView(viewsets.ModelViewSet):
    queryset = UserExamDetail.objects.all()
    serializer_class = UserExamDetailSerializer
    # lookup_field='id'

    # for custom handling of http method 'post' override the
    # create() function and write your custom logic
    # you can find more from 'http://cdrf.co'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.perform_create(serializer)
        response = serializer.data

        return Response(
            data={
                'status': True,
                'message': "User-Exam saved",
                'data': response
            },
            status=status.HTTP_201_CREATED
        )

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            # PAGINATION PURPOSE
            # We are setting default number of items per page = 40
            # By default we set starting index 0 and ending index 39 (index=9 means serially 10th item) [see python data slicing mechanism to know more ]
            page_number = self.request.query_params.get('page')
            number_of_items_per_page = self.request.query_params.get(
                'items')
            # Although user can request for number_of_items_per_page via the url, we set it default 40
            items_per_page = 40
            start = 0
            end = items_per_page

            if(page_number != None and number_of_items_per_page != None):
                start = int(number_of_items_per_page) * \
                    int(page_number) - int(number_of_items_per_page)
                end = int(number_of_items_per_page) * int(page_number)

            elif(page_number != None and number_of_items_per_page == None):
                start = items_per_page * int(page_number) - items_per_page
                end = items_per_page * int(page_number)

            elif(page_number == None and number_of_items_per_page != None):
                # Since user didn't give page_number, we assume he wants the first page (i,e page_number = 1)
                start = int(number_of_items_per_page) * 1 - \
                    int(number_of_items_per_page)
                end = int(number_of_items_per_page) * 1

            if(page_number == None):
                page_number = 1

            queryset = queryset[start:end]

            serializer = self.get_serializer(queryset, many=True)
            return Response(
                data={
                    'status': True,
                    'page_number': page_number,
                    'total': len(serializer.data),
                    'message': "All exams",
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception as ex:
            return Response(
                data={
                    'status': False,
                    'message': "Something wrong"
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # above line will create an instance with the provided 'id' in the url. Since, we
            # setup 'lookup_field=id', it will search the 'id' column with the provided id.

            # serializing the queryied data
            serializer = self.get_serializer(instance)
            return Response(
                data={
                    'status': True,
                    'message': "Exam information",
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception as ex:
            return Response(
                data={
                    'status': False,
                    'message': "Exam not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )


class LoginView(CreateAPIView):
    def create(self, request, *args, **kwargs):
        mobile_number = request.data['mobile']
        password = request.data['password']
        data = User.objects.get(mobile=mobile_number)

        if(data.password == password):
            return Response(
                data={
                    'message': 'Valid User',
                    'status': True,
                    'data': {
                        "userId": data.id,
                        "name": data.name,
                        "mobile": data.mobile,
                    }
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={
                    'message': 'Login failed',
                    'status': False,
                },
                status=status.HTTP_401_UNAUTHORIZED
            )


class SignupView(CreateAPIView):
    def create(self, request, *args, **kwargs):
        name = request.data['name']
        mobile_number = request.data['mobile']
        password = request.data['password']
        data = User.objects.create(
            name=name, mobile=mobile_number, password=password)

        if(data.password == password):
            return Response(
                data={
                    'message': 'User created successfully !',
                    'status': True,
                    'data': {
                        "userId": data.id,
                        "name": data.name,
                        "mobile": data.mobile,
                    }
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                data={
                    'message': 'Singup failed',
                    'status': False,
                },
                status=status.HTTP_401_UNAUTHORIZED
            )


# class FetchQuestionView(RetrieveAPIView):
#     def get(self, request, *args, **kwargs):
#         userId = kwargs['userId']
#         examId = kwargs['examId']
#         data = Question.objects.filter(fk=mobile_number)

#         if(data.password == password):
#           return Response(
#               data={
#                   'message': 'Valid User',
#                   'status': True
#               },
#               status=status.HTTP_200_OK
#           )
#         else:
#           return Response(
#               data={
#                   'message': 'Login failed',
#                   'status': False,
#               },
#               status=status.HTTP_401_UNAUTHORIZED
#           )
