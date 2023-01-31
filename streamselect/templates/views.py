import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from repository.models import (Crop,
                               Disease,
                               Symptoms,
                               Agent,
                               SymptomsImage,
                               CultureImage,
                               AgentImage,
                               UserProfileInfo)
from repository.constants import (STATUS_CODE_METHOD_NOT_ALLOWED, STATUS_CODE_UNAUTHORIZED)

from repository.responses.general_response import (INVALID_SESSION_RESPONSE,
                                                   no_success_response,
                                                   success_response)
from repository.utility.utility import is_mobile_request, base64StringToInMemoryImage


def create_crop(request):
    user = request.user

    if not request.user.is_authenticated:
        return HttpResponse(json.dumps(INVALID_SESSION_RESPONSE))
    else:
        if request.POST.get('cropname') and request.POST.get('family') and request.POST.get('plantpart'):
            if request.method == 'POST':
                cropmodel = Crop()
                cropmodel.crop_name = request.POST.get('cropname')
                cropmodel.crop_family = request.POST.get('family')
                cropmodel.plant_part = request.POST.get('plantpart')
                cropmodel.added_by = UserProfileInfo.objects.get(username=user.username)
                cropmodel.save()
                response = success_response()
                response['success_message'] = "Crop added successfully"
                return render(request, 'repository/create_crop.html', response)
            else:
                response = no_success_response()
                response['error_message'] = "Invalid Data"
                if is_mobile_request(request):
                    HttpResponse(json.dumps(response))
                else:
                    return render(request, 'repository/create_crop.html', response)
    return render(request, 'repository/create_crop.html')


def view_crop_detail(request):
    if not request.user.is_authenticated:
        return HttpResponse(json.dumps(INVALID_SESSION_RESPONSE))
    all_crop = Crop.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(all_crop, 5)
    try:
        allcrop = paginator.page(page)
    except PageNotAnInteger:
        allcrop = paginator.page(1)
    except EmptyPage:
        allcrop = paginator.page(paginator.num_pages)

    return render(request, 'repository/crop_list.html', {'all_crops': allcrop})


def delete_crop(request):
    crop_id = request.POST.get('crop_id')
    if crop_id:
        crop = Crop.objects.get(id=crop_id)
        if crop:
            crop.delete()
            response = success_response()
            response['message'] = 'Data deleted successfully'
        else:
            response = no_success_response()
            response['message'] = 'crop not found with crop id %s' % (crop_id)
    else:
        response = no_success_response()
        response['message'] = 'not valid crop id given %s' % (crop_id)
    return HttpResponse(json.dumps(response))


def edit_crop(request):
    user = request.user
    if not request.user.is_authenticated:
        return HttpResponse(json.dumps(INVALID_SESSION_RESPONSE), status_code=STATUS_CODE_UNAUTHORIZED)
    crop_id = request.POST.get('crop_id')
    if crop_id:
        crop = Crop.objects.get(id=crop_id)
        if crop:
            crop_family = request.POST.get('family')
            plant_part = request.POST.get('plantpart')
            crop_name = request.POST.get('name')
            if crop_name:
                crop.crop_name = crop_name
            if crop_family:
                crop.crop_family = crop_family
            if plant_part:
                crop.plant_part = plant_part
            crop.save()
            response = success_response()
            response['message'] = 'Successfully updated crop with crop id %s' % (crop_id)
        else:
            response = no_success_response()
            response['message'] = 'Valid Crop not found for this crop id %s' % (crop_id)
    else:
        response = no_success_response()
        response['message'] = 'not valid crop id given %s' % (crop_id)

    return HttpResponse(json.dumps(response))


def create_disease(request):
    user = request.user
    if not request.user.is_authenticated:
        return HttpResponse(json.dumps(INVALID_SESSION_RESPONSE))

    if request.method == 'POST':
        if request.POST.get('crop_id') and request.POST.get('dis_name') and request.POST.get('description') and \
                request.POST.get('category') and request.POST.get('measures') and request.POST.get('month') \
                and request.POST.get('condition'):
            crop_id = request.POST.get('crop_id')
            crop = Crop.objects.get(id=int(crop_id))
            if not crop:
                response = no_success_response()
                response['error_message'] = 'Valid crop not found for crop id %s' % (crop_id)
                if is_mobile_request(request):
                    HttpResponse(json.dumps(response))
                else:
                    return render(request, 'repository/create_disease.html', response)
            else:
                diseasemodel = Disease()
                diseasemodel.added_by = UserProfileInfo.objects.get(username=user.username)
                diseasemodel.crop = crop
                diseasemodel.name = request.POST.get('dis_name')
                diseasemodel.category = request.POST.get('category')
                diseasemodel.desc = request.POST.get('description')
                diseasemodel.measures = request.POST.get('measures')
                diseasemodel.month = request.POST.get('month')
                diseasemodel.condition = request.POST.get('condition')
                diseasemodel.save()
                response = success_response()
                response['success_message'] = "Disease added successfully"
                return render(request, 'repository/create_disease.html', response)
        else:
            response = no_success_response()
            response['error_message'] = "Valid data not given"
            if is_mobile_request(request):
                HttpResponse(json.dumps(response))
            else:
                return render(request, 'repository/create_disease.html', response)
    else:
        all_crops = Crop.objects.all()
        if all_crops:
            response = success_response()
            response['all_crops'] = [crop.embed("ID") for crop in all_crops]
        else:
            response = no_success_response()
            response[
                'error_message'] = "There is no crop added into the system. Please add crop first and then add disease"
    return render(request, 'repository/create_disease.html', response)


def edit_disease(request):
    user = request.user
    if not request.user.is_authenticated:
        return HttpResponse(json.dumps(INVALID_SESSION_RESPONSE), status_code=STATUS_CODE_UNAUTHORIZED)
    host_id = request.POST.get('host_id')
    if host_id:
        host = Disease.objects.get(id=host_id)
        if host:
            crop_family = request.POST.get('family')
            plant_part = request.POST.get('plantpart')
            crop_name = request.POST.get('name')
            if crop_name:
                host.crop_name = crop_name
            if crop_family:
                host.crop_family = crop_family
            if plant_part:
                host.plant_part = plant_part
            host.save()
            response = success_response()
            response['message'] = 'Successfully updated disease with disease id %s' % (host_id)
        else:
            response = no_success_response()
            response['message'] = 'Valid Disease not found for this disease id %s' % (host_id)
    else:
        response = no_success_response()
        response['message'] = 'not valid disease id given %s' % (host_id)

    return HttpResponse(json.dumps(response))


def delete_disease(request):
    disease_id = request.POST.get('crop_id')
    if disease_id:
        disease = Disease.objects.get(id=disease_id)
        if disease:
            disease.delete()
            response = success_response()
            response['message'] = 'Data deleted successfully'
        else:
            response = no_success_response()
            response['message'] = 'Disease not found with Disease id %s' % (disease_id)
    else:
        response = no_success_response()
        response['message'] = 'Not valid Disease id given %s' % (disease_id)
    return HttpResponse(json.dumps(response))


def view_disease_detail(request, crop_id):
    if not request.user.is_authenticated:
        return HttpResponse(json.dumps(INVALID_SESSION_RESPONSE))

    all_disease = Disease.objects.filter(crop=crop_id)
    return render(request, 'repository/disease_list.html', {'host_list': all_disease})


def create_symptoms(request):
    user = request.user
    if not request.user.is_authenticated:
        return HttpResponse(json.dumps(INVALID_SESSION_RESPONSE))

    mobile_request = is_mobile_request(request)
    print("is mobile request=", mobile_request)

    response = no_success_response()
    if request.method == 'POST':
        if request.POST.get('disease_id') and request.POST.get('symptoms') \
                and request.FILES.getlist('symp_image') and request.POST.get('cult_detail') \
                and request.FILES.getlist('cult_image'):
            disease_id = request.POST.get('disease_id')
            disease = Disease.objects.get(id=int(disease_id))
            if not disease:
                response = no_success_response()
                response['error_message'] = 'Valid disease not found for disease id %s' % (disease_id)
            else:
                if mobile_request:
                    if request.POST.get('symp_image') and request.POST.get('cult_image'):
                        symp_image = [base64StringToInMemoryImage(request.POST.get('symp_image'))]
                        cult_image = [base64StringToInMemoryImage(request.POST.get('cult_image'))]
                    else:
                        response = no_success_response()
                        response['error_message'] = "Base64 image string does not provided"
                        return HttpResponse(json.dumps(response))
                else:
                    if request.FILES.getlist('symp_image') and request.FILES.getlist('cult_image'):
                        symp_image = request.FILES.getlist('symp_image')
                        cult_image = request.FILES.getlist('cult_image')
                    else:
                        response = no_success_response()
                        response['error_message'] = "Not valid images given"
                        return render(request, 'repository/create_agent.html', response)

                symptomsmodel = Symptoms()
                symptomsmodel.disease = disease
                symptomsmodel.added_by = UserProfileInfo.objects.get(username=user.username)
                symptomsmodel.symptom = request.POST.get('symptoms')
                symptomsmodel.culture_detail = request.POST.get('cult_detail')
                symptomsmodel.save()

                symptomsmodel = Symptoms.objects.get(symptom=request.POST.get('symptoms'))
                for image in symp_image:
                    synimagem = SymptomsImage()
                    synimagem.symptom = symptomsmodel
                    synimagem.dis_image = image
                    synimagem.dis_image_ext = image.name.split('.')[-1]
                    synimagem.save()

                for image in cult_image:
                    cultimagem = CultureImage()
                    cultimagem.symptom = symptomsmodel
                    cultimagem.culture_image = image
                    cultimagem.culture_image_ext = image.name.split('.')[-1]
                    cultimagem.save()
            response = success_response()
            response['success_message'] = "Added successfully"
            if mobile_request:
                return HttpResponse(json.dumps(response))
            else:
                return render(request, 'repository/create_symptoms.html', response)
        else:
            response = no_success_response()
            response['error_message'] = "Valid data not given"
            if mobile_request:
                return HttpResponse(json.dumps(response))
            else:
                return render(request, 'repository/create_symptoms.html', response)
    else:
        all_diseases = Disease.objects.all()
        if all_diseases:
            response = success_response()
            response['all_diseases'] = [disease.embed("ID") for disease in all_diseases]
        else:
            response = no_success_response()
            response[
                'error_message'] = "There is no disease added into the system. Please add disease first and then add symptoms"
            if mobile_request:
                return HttpResponse(json.dumps(response))
            else:
                return render(request, 'repository/create_symptoms.html', response)
    return render(request, 'repository/create_symptoms.html', response)


def create_agent(request):
    user = request.user
    if not request.user.is_authenticated:
        return HttpResponse(json.dumps(INVALID_SESSION_RESPONSE))

    mobile_request = is_mobile_request(request)
    print("is mobile request=", mobile_request)

    response = no_success_response()
    if request.method == 'POST':
        if request.POST.get('disease_id') and request.POST.get('agent_name') \
                and request.POST.get('agent_detail'):
            if mobile_request:
                if request.POST.get('agent_image'):
                    agent_image = [base64StringToInMemoryImage(request.POST.get('agent_image'))]
                else:
                    response = no_success_response()
                    response['error_message'] = "Base64 image string does not provided"
                    return HttpResponse(json.dumps(response))
            else:
                if request.FILES.getlist('agent_image'):
                    agent_image = request.FILES.getlist('agent_image')
                else:
                    response = no_success_response()
                    response['error_message'] = "Not valid images given"
                    return render(request, 'repository/create_agent.html', response)

            disease_id = request.POST.get('disease_id')
            disease = Disease.objects.get(id=int(disease_id))
            if not disease:
                response = no_success_response()
                response['error_message'] = 'Valid disease not found for disease id %s' % (disease_id)
            else:
                agentmodel = Agent()
                agentmodel.disease = disease
                # agentmodel.added_by = UserProfileInfo.objects.get(username=user.username)
                agentmodel.added_by = UserProfileInfo.objects.get(username=user.username)
                agentmodel.agent_name = request.POST.get('agent_name')
                agentmodel.agent_detail = request.POST.get('agent_detail')
                agentmodel.save()

                agentmodel = Agent.objects.get(agent_name=request.POST.get('agent_name'))
                for image in agent_image:
                    agentimagem = AgentImage()
                    agentimagem.agent = agentmodel
                    agentimagem.agent_image = image
                    agentimagem.agent_image_ext = image.name.split('.')[-1]
                    agentimagem.save()

                response = success_response()
                response['success_message'] = "Added successfully"
                if mobile_request:
                    return HttpResponse(json.dumps(response))
                else:
                    return render(request, 'repository/create_agent.html', response)
        else:
            response['error_message'] = "Invalid Data given for disease and agent"
            if mobile_request:
                return HttpResponse(json.dumps(response))
            else:
                return render(request, 'repository/create_agent.html', response)
    else:
        all_diseases = Disease.objects.all()
        if all_diseases:
            response = success_response()
            response['all_diseases'] = [disease.embed("ID") for disease in all_diseases]
        else:
            response = no_success_response()
            response[
                'error_message'] = "There is no disease added into the system. Please add disease first and then add agents"
        if mobile_request:
            return HttpResponse(json.dumps(response))
        else:
            return render(request, 'repository/create_agent.html', response)
    return render(request, 'repository/create_agent.html', response)


def view_symptom_agent_detail(request, disease_id):
    if not request.user.is_authenticated:
        return HttpResponse(json.dumps(INVALID_SESSION_RESPONSE))

    all_symptom = Symptoms.objects.filter(disease=disease_id)
    all_symptoms_data = []
    for symptom in all_symptom:
        all_symptoms_data.append(symptom.embed())
    all_agent = Agent.objects.filter(disease=disease_id)
    all_agent_data = []
    for agent in all_agent:
        all_agent_data.append(agent.embed())
    return render(request, 'repository/symptoms_agent_list.html',
                  {'symptoms_list': all_symptoms_data, 'agent_list': all_agent_data})
