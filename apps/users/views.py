from django.shortcuts import render, get_object_or_404, redirect
from requests import post
from .models import User, TrainData, TrainVersion
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.conf import settings


import csv
from django.core.files.base import ContentFile
from django.utils.text import slugify
import base64
import json
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential, load_model
from keras.layers import Dense





def register(request):
    if request.method == 'POST':
        # Get the user data from the request
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        # Create a new user
        user = User.objects.create_user(username, username, password)
        user.save()
        # Log the user in after registration
        login(request, user)
        return redirect('dashboard')  # Replace 'success_page' with the actual URL for a successful registration

    return render(request, 'register.html')

def login_view(request):
    data = request.GET
    url = 'dashboard'
    if request.method == 'POST':
        email = request.POST['email']  # Change 'username' to 'email'
        password = request.POST['password']
        user = authenticate(username=email, password=password)  # Authenticate with email

        if user is not None:
            login(request, user)
            return redirect(url)  # Replace 'dashboard' with the URL name of your dashboard view
        else:
            print("No estás logeado")  # Handle login failure

    return render(request, 'registration/login.html')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')


@login_required
def dashboard(request):
    # Retrieve all TrainVersion instances
    train_versions = TrainVersion.objects.all()

    return render(request, 'dashboard.html', {'train_versions': train_versions})

@login_required
def train_version_detail(request, train_version_id):
    # Get the TrainVersion instance or return a 404 error if not found
    train_version = get_object_or_404(TrainVersion, pk=train_version_id)

    return render(request, 'train_version_detail.html', {'train_version': train_version})


def create_train_data(request):
    if request.method == 'POST':
        custom_name = request.POST['custom_name']
        version = request.POST['version']
        data_file = request.FILES['data']

        # Create TrainVersion instance
        train_version = TrainVersion.objects.create(
            custom_name=custom_name,
            version=version,
            trained=False  # Assuming trained should be set to False by default
        )

        # Create TrainData instance and associate it with the TrainVersion
        train_data = TrainData(version=train_version, data=data_file)
        # train_data.train_version = train_version
        train_data.save()

        # Process the CSV file (you may adjust this based on your CSV structure)
        csv_data = data_file.read().decode('utf-8').splitlines()
        csv_reader = csv.DictReader(csv_data)

        return HttpResponse('Data saved successfully!')

    return HttpResponse('Invalid request method.')


def train_model(request):
    if request.method == 'POST':
        # Get the train_version_id from the POST data
        train_version_id = request.POST.get('train_version_id')

        # Check if the TrainVersion exists
        try:
            train_version = TrainVersion.objects.get(pk=train_version_id)
        except TrainVersion.DoesNotExist:
            return HttpResponse(f'TrainVersion with id {train_version_id} does not exist.', status=404)

        # Construct the file path for the CSV file based on the train_version_id
        csv_file_path = os.path.join('media', 'train_data', f'{train_version_id}.csv')

        # Check if the file exists
        if os.path.exists(csv_file_path):
            # Load data from the CSV file
            df = pd.read_csv(csv_file_path)
            df = df.iloc[:, 1:]
            df = df.replace(to_replace='\((.*?)\)', value='-', regex=True)
            df = df.replace(',', '.', regex=True)
            df = df.apply(pd.to_numeric, errors='coerce')
            df = df.dropna()

            # Split data
            X = df.iloc[:, :-1].values
            y = df.iloc[:, -1].values

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Normalize data
            scaler = StandardScaler()
            X_train = scaler.fit_transform(X_train)
            X_test = scaler.transform(X_test)

            # Build the model and perform training as you did before
            model = Sequential()
            model.add(Dense(64, input_dim=8, activation='relu'))
            model.add(Dense(32, activation='relu'))
            model.add(Dense(16, activation='relu'))
            model.add(Dense(1, activation='linear'))

            model.compile(loss='mean_squared_error', optimizer='adam')

            history = model.fit(X_train, y_train, epochs=250, batch_size=32, validation_data=(X_test, y_test), verbose=2)

            # Evaluate the model
            loss = model.evaluate(X_test, y_test)
            print(f'Loss on test data: {loss}')

            # Save the trained model
            model.save(f'media/models/model_{train_version_id}.keras')

            # Get the final loss value from the training history
            final_loss = history.history['val_loss'][-1]

            # Update the TrainVersion instance with the final loss value and set trained to True
            train_version.loss = final_loss
            train_version.trained = True
            train_version.save()

            return HttpResponse('Training completed successfully.')

        else:
            return HttpResponse(f'CSV file for train_version_id {train_version_id} not found.', status=404)

    return HttpResponse('Nothing.')


def prediction_model(request):
    if request.method == 'POST':
        # Get the input values from the POST data
        x1 = float(request.POST.get('x1'))
        x2 = float(request.POST.get('x2'))
        x3 = float(request.POST.get('x3'))
        x4 = float(request.POST.get('x4'))
        x5 = float(request.POST.get('x5'))
        x6 = float(request.POST.get('x6'))
        x7 = float(request.POST.get('x7'))
        x8 = float(request.POST.get('x8'))

        # Get the versionId from the POST data
        version_id = request.POST.get('versionId')

        # Construct the file path for the trained model based on the versionId
        # model_file_path = f'media/models/model_{version_id}.keras'
        model_file_path = os.path.join('media', 'models', f'model_{version_id}.keras')

        # Check if the model file exists
        if os.path.exists(model_file_path):
            # Load the trained model
            loaded_model = load_model(model_file_path)
            csv_file_path = os.path.join('media', 'train_data', f'{version_id}.csv')

            # Cargar el StandardScaler desde su archivo (asegúrate de tener el archivo guardado)
            scaler = StandardScaler()
            scaler = scaler.fit(pd.read_csv(csv_file_path).iloc[:, 1:].replace(to_replace='\((.*?)\)', value='-', regex=True).replace(',', '.', regex=True).apply(pd.to_numeric, errors='coerce').dropna().iloc[:, :-1].values)


            # Prepare the input data for prediction
            input_data = np.array([[x1, x2, x3, x4, x5, x6, x7, x8]])
            input_data_scaled = scaler.transform(input_data)

            # Make predictions with the loaded model
            # prediction_scaled = loaded_model.predict(input_data_scaled)[0][0]
            # prediction_original = scaler.inverse_transform([[0, 0, 0, 0, 0, 0, 0, prediction_scaled]])[0][7]
            prediction_scaled = float(loaded_model.predict(input_data_scaled)[0][0])
            prediction_original = float(scaler.inverse_transform([[0, 0, 0, 0, 0, 0, 0, prediction_scaled]])[0][7])

            # Return the prediction result as JSON
            return JsonResponse({'prediction_scaled': prediction_scaled, 'prediction_original': prediction_original})
        else:
            return JsonResponse({'error': f'Model file for versionId {version_id} not found.'}, status=404)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)





# @login_required
# def dashboard(request):
#     client_id = settings.CLIENT_ID
#     client_secrect = settings.CLIENT_SECRECT
#     # token = get_token(client_id, client_secrect)
#     print(token)

#     return render(request, 'dashboard.html')


# def get_token(client_id, client_secrect):
#     auth_string = client_id + ':' + client_secrect
#     auth_bytes = auth_string.encode("utf-8")
#     auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
#     url = "https://accounts.spotify.com/api/token"
#     headers = {
#         "Authorization": "Basic "+ auth_base64,
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
#     data = {"grant_type": "client_credentials"}
#     result = post(url, headers=headers, data=data)
#     json_result = json.loads(result.content)
#     token = json_result["access_token"]
#     return token

# def get_auth_header(token):

#     return {"Authorization": "Bearer " + token}