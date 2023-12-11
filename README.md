# BLOG RESTAPI

**First edition of FastAPI BLOG RestAPI has been completely upgraded**

1. based on the latest version of FastAPI 0.104.1
2. Pipenv painless management of virtual environments and dependencies
3. more simple and painless deployment process, a few commands quickly online, a key script painless updates

- [E-COMMERCE REST API](git@github.com:EnocDelgado/Blog-RestAPI-FastAPI.git)

--------

The code for each tutorial is located in the corresponding branch of the project, which can be viewed by clicking on the **Branch** button above, e.g. the branch Step1_build-development-environment corresponds to the rest api

The master branch is the complete code of the project.

## Running the project locally

1. Clone the project locally

   Open the command line, go to the folder where you saved the project, and enter the following command:

   ```
   git clone git@github.com:EnocDelgado/Blog-RestAPI-FastAPI.git
   ```

2. Create and activate a virtual environment

   At the command line, go to the folder where the virtual environment is saved and enter the following command to create and activate the virtual environment:

   ```
   python3 -m venv <name>

   # windows
   python -m venv <name>

   # linux or Mac
   python3 -m venv <name>
   ```

3. Install project dependencies

   If you are using a virtual environment, make sure it is activated and accessible by going to the E-commerce-RestAPI-FastAPI folder of your project at the command line and running the following command:

   ```
   pip install -r requirements.txt
   ```

4. Run the project

   To start the project, run the following command in the same location as in the previous step:

   ```
   uvicorn app.main:app --reload
   ```

5. Use End points

    With tools such as Postman or Thunder Client, test the EndPoints of this application.

6. Deactive Environment

    At the console run the following command
    ```
    deactivate
    ```