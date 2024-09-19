# UniFi Tuner



## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)


## Introduction

**UniFi Tuner** is an intelligent automation tool built using Python and the Autogen AI Agent framework. It leverages advanced AI agents to automate various tasks, enhancing efficiency and productivity. This project focuses on creating modular and maintainable code to manage and deploy multiple AI agents effectively.

## Features

- **Modular AI Agents:** That asses the network and make recommendations on how to improve the network and also human in the loop agent to continue to ask clarifying questions on recommendations. 
- **Environment Configuration:** Securely manage API keys and model configurations using a `.env` file.
- **Group Chat Management:** Efficiently handle group chat interactions with multiple agents.
- **Logging & Error Handling:** Comprehensive logging for better debugging and error management.
- **Scalable Architecture:** Designed for scalability and ease of maintenance.

## Technologies Used


- **AI Framework:** Autogen AI Agent
- **Environment Management:** `python-dotenv`
- **Version Control:** Git

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python 3.12** installed on your machine. You can download it from [here](https://www.python.org/downloads/).
- **Git** installed for version control. Download it from [here](https://git-scm.com/downloads).
- An **OpenAI API Key**. Sign up and obtain your API key from [OpenAI](https://platform.openai.com/signup).
- Create a local account on your unifi dream machine or controller and obtain the api credentials.

## Installation

Follow these steps to set up the project locally:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/unifi_tuner.git
   cd unifi_tuner
   ```

2. **Create a Virtual Environment**

   It's recommended to use a virtual environment to manage dependencies.

   ```bash
   python3 -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   *Ensure that your `requirements.txt` includes all necessary packages, such as `python-dotenv`, `autogen`, `flask`, etc.*

## Configuration

1. **Set Up Environment Variables**

   Create a `.env` file in the root directory of the project and add the following configurations:

   

   *Ensure that `.env` is included in your `.gitignore` to prevent sensitive information from being committed.*

2. **Update `.gitignore`**

   Your `.gitignore` should exclude unnecessary files and directories. Ensure it includes the following:

   ```gitignore:unifi_tuner/.gitignore
   # Ignore all JSON files
   *.json

   # Ignore recommendations.txt
   recommendations.txt

   # Ignore virtual environment directory
   myenv/

   # Ignore cache directories
   .cache/
   __pycache__/

   # Ignore simple_autogenexample.py
   simple_autogenexample.py
   ```

## Usage

1. **Activate the Virtual Environment**

   ```bash
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   ```

2. **Run the Application**

   Execute the main Python script to start the AI agents and manage group chat interactions.

   ```bash
   python unifi_ai_agents.py
   ```

3. **Logging**

   Logs are configured to display informational messages. Monitor the console output to observe interactions and identify any potential issues.

   ## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. **Fork the Repository**

2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add some feature"
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**

   Describe your changes and submit the pull request for review.

## License

This project is licensed under the [Apache License 2.0](LICENSE). You are free to use, modify, and distribute it as per the terms of the license. For more details, refer to the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

**Additional Steps to Apply the Apache License 2.0:**

1. **Create a `LICENSE` File**

   Add the full text of the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt) to a file named `LICENSE` in the root directory of your project.

2. **Create a `NOTICE` File** *(Optional but Recommended)*

   If your project includes a `NOTICE` file as part of its distribution, ensure that it contains the necessary attribution notices.

   ```markdown:unifi_tuner/NOTICE
   Ramda Adjunct
   Copyright 2017, Vladimír Gorej
   ```

   Refer to the [Apache License 2.0 guidelines](https://www.apache.org/licenses/LICENSE-2.0.txt) for more information on the `NOTICE` file.

## Contact

For any questions or suggestions, feel free to contact me:

- **Email:** 
- **LinkedIn:** [linkedin.com/in/damonmcdougald](https://www.linkedin.com/in/damon-m-4b60a14a/)
