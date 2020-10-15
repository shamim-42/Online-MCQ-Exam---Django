from django.http import HttpResponse
from datetime import datetime, timedelta
from django.conf import settings
import jwt
import json
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
from auth import authenticate_credentials, decode_jwt


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # lookup_field='id'

    # for custom handling of http method 'post' override the
    # create() function and write your custom logic
    # you can find more from 'http://cdrf.co'

    def create(self, request, *args, **kwargs):
        if authenticate_credentials(request.headers["Authorization"]):
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
        if authenticate_credentials(request.headers["Authorization"]):

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
        if authenticate_credentials(request.headers["Authorization"]):
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
        if authenticate_credentials(request.headers["Authorization"]):
            have_enough_permission = decode_jwt(
                request.headers["Authorization"])['data']['isSuperuser']

            if have_enough_permission:
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
            else:
                return Response(
                    data={
                        'status': False,
                        'message': "You don't have enough permission to create an exam",
                        'data': ""
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

    def list(self, request, *args, **kwargs):
        if authenticate_credentials(request.headers["Authorization"]):
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
        if authenticate_credentials(request.headers["Authorization"]):

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
        if authenticate_credentials(request.headers["Authorization"]):

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
        if authenticate_credentials(request.headers["Authorization"]):

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
        if authenticate_credentials(request.headers["Authorization"]):

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
        if authenticate_credentials(request.headers["Authorization"]):

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

        else:
            return Response(
                data={
                    'status': False,
                    'message': "no_jwt_token",
                    'data': ""
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

    def list(self, request, *args, **kwargs):
        if authenticate_credentials(request.headers["Authorization"]):
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

                myqueryset = queryset.values()
                all_exams = Exam.objects.all()
                for i in myqueryset:
                    i['exam_name'] = all_exams.get(id=i['fk_exam_id']).title

                serializer = self.get_serializer(myqueryset, many=True)

                return Response(
                    data={
                        'status': True,
                        'page_number': page_number,
                        'total': len(serializer.data),
                        'message': "all_exam",
                        'data': myqueryset
                    },
                    status=status.HTTP_200_OK
                )

            except Exception as ex:
                return Response(
                    data={
                        'status': False,
                        'message': "Something wrong",
                        'error': ex
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                data={
                    'status': False,
                    'message': "unauthorized",
                    'data': ""
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

    def retrieve(self, request, *args, **kwargs):
        if authenticate_credentials(request.headers["Authorization"]):

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
        if authenticate_credentials(request.headers["Authorization"]):
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
        if authenticate_credentials(request.headers["Authorization"]):
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
        if authenticate_credentials(request.headers["Authorization"]):
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
            payload = {
                "mobile": mobile_number,
                "name": data.name,
                "userId": data.id,
                "isSuperuser": data.is_superuser,
            }
            jwt_token = jwt.encode(
                {
                    "data": payload,
                    "exp": datetime.utcnow() + timedelta(seconds=60*60*int(settings.JWT_SECRET_KEY_VALID_IN_HOUR))
                },
                settings.JWT_SECRET_KEY, algorithm='HS256').decode('utf-8')

            return Response(
                data={
                    'message': 'Valid User',
                    'status': True,
                    'data': {
                        "userId": data.id,
                        "name": data.name,
                        "mobile": data.mobile,
                        "jwt_token": jwt_token
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

        existance = User.objects.filter(mobile=mobile_number)
        if(len(existance) > 0):
            return Response(
                data={
                    'message': 'Already exists',
                    'status': False,
                },
                status=status.HTTP_409_CONFLICT
            )
        else:

            data = User.objects.create(
                name=name, mobile=mobile_number, password=password)

            if(data.password == password):
                payload = {
                    "mobile": mobile_number,
                    "name": data.name,
                    "userId": data.id,
                    "isSuperuser": data.is_superuser,
                }
                jwt_token = jwt.encode(
                    {
                        "data": payload,
                        "exp": datetime.utcnow() + timedelta(seconds=60*60*int(settings.JWT_SECRET_KEY_VALID_IN_HOUR))
                    },
                    settings.JWT_SECRET_KEY, algorithm='HS256').decode('utf-8')

                return Response(
                    data={
                        'message': 'User created successfully !',
                        'status': True,
                        'data': {
                            "userId": data.id,
                            "name": data.name,
                            "mobile": data.mobile,
                            "jwt": jwt_token
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


class AnswerEvaluation(CreateAPIView):
    def create(self, request,  *args, **kwargs):
        if authenticate_credentials(request.headers["Authorization"]):
            try:
                userAnswers = request.data['selectedAnswer']
                exam_id = request.data['examId']
                user_id = request.data['userId']
                taken_time = request.data['taken_time']  # in minutes

                user = User.objects.get(id=user_id)  # creating instance
                exam = Exam.objects.get(id=exam_id)  # creating instance

                # if already answered then don't go ahead to save again same question
                queryset = UserExam.objects.filter(fk_user=user, fk_exam=exam)

                if (len(queryset.values()) == 0):
                    queryset = Question.objects.filter(fk_exam=exam_id)
                    achieved_marks = 0
                    all_ques = queryset.values()
                    total_question = len(all_ques)

                    for i in userAnswers:
                        q_id = i['question_id']
                        user_selected = i['selected_answer']

                        the_question = all_ques.filter(id=q_id)
                        correct_option = the_question[0]['correct_option']

                        if user_selected == correct_option:
                            achieved_marks += the_question[0]['marks']

                    obj = UserExam(total_question=total_question, achieved_marks=achieved_marks,
                                   status="done", fk_user=user, fk_exam=exam, taken_time=taken_time)
                    obj.save()

                    return(
                        Response(
                            data={
                                "message": "exam_result",
                                "status": True,
                                "data": {
                                    "achieved_marks": achieved_marks
                                }
                            })
                    )

                else:
                    return(
                        Response(
                            data={
                                "status": False,
                                "message": "already_given",
                                "data": ""
                            })
                    )

            except Exception as ex:

                return(
                    Response(
                        data={
                            "status": False,
                            "message": "error",
                            "data": "",
                            "error": ex,
                        })
                )
        else:
            return(
                Response(
                    data={
                        "status": False,
                        "message": "send valid token",
                        "data": ""
                    })
            )


class MakeSuperuser(CreateAPIView):
    def create(self, request, *args, **kwargs):
        if authenticate_credentials(request.headers["Authorization"]):
            have_enough_permission = decode_jwt(
                request.headers["Authorization"])['data']['isSuperuser']
            if(have_enough_permission):

                proposed_user = request.data['proposedUserId']
                try:
                    obj = User.objects.get(id=proposed_user)
                    obj.is_superuser = True
                    obj.save()

                    return(
                        Response(
                            data={
                                "status": True,
                                "message": "user_is_now_superuser",
                                # "data": obj
                            })
                    )
                except:
                    return(
                        Response(
                            data={
                                "status": False,
                                "message": "error",
                                "data": ""
                            })
                    )
            else:
                return(
                    Response(
                        data={
                            "status": False,
                            "message": "You don't have enough permission to make another superuser",
                            "data": ""
                        }
                    )
                )
        else:
            return(
                Response(
                    data={
                        "status": False,
                        "message": "No JWT token provided",
                        "data": ""
                    }
                )
            )


class RemoveSuperuser(CreateAPIView):
    def create(self, request, *args, **kwargs):
        if authenticate_credentials(request.headers["Authorization"]):
            have_enough_permission = decode_jwt(
                request.headers["Authorization"])['data']['isSuperuser']

            if(have_enough_permission):

                proposed_user = request.data['proposedUserId']

                try:
                    obj = User.objects.get(id=proposed_user)
                    obj.is_superuser = False
                    obj.save()

                    return(
                        Response(
                            data={
                                "status": True,
                                "message": "user_is_no_longer_superuser",
                                # "data": obj
                            })
                    )
                except:
                    return(
                        Response(
                            data={
                                "status": False,
                                "message": "error",
                                "data": ""
                            })
                    )
            else:
                return(
                    Response(
                        data={
                            "status": False,
                            "message": "You don't enough permission to remove another from superuser",
                            "data": ""
                        })
                )
        else:
            return(
                Response(
                    data={
                        "status": False,
                        "message": "No JWT token provided",
                        "data": ""
                    }
                )
            )
