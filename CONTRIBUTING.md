# Contributing to the Teams Bot Repository

Thank you for your interest in contributing to our Teams Bot! This document provides guidelines and steps for setting up and contributing new bots to the repository.

## Getting Started

Before contributing, please ensure you have a setup that includes Python, Git, and appropriate access rights to the repository. Familiarize yourself with the structure of the project and the configuration files.

## Contribution Steps

To contribute a new bot, follow these detailed steps:

### 1. Create Bot File

- Navigate to the `Bots` folder.
- Create a new file named `{Site_name}.py`.
- Copy the template code from an existing bot file in this folder.
- Modify the copied template by changing the Bot name, Site name, and any relevant prompts specific to the new bot.

### 2. Define New Prompts

- Open the `prompts.py` file.
- Copy an existing prompt function and paste it as a new function.
- Modify the copied prompt to reflect the new Site name and any other specific requirements.

### 3. Update Environment Variables

- Go to the `.env` file in the root directory.
- Add the new Microsoft ID and password for the new bot, ensuring these credentials are secure.

### 4. Configure the Bot

- Open the `config.py` file.
- Create a new configuration section for your bot, defining all necessary parameters and settings.

### 5. Set Up the Bot in the main file

- Open the `app.py` file.
- Create a new bot adapter by copying an existing one and modifying it as required for the new bot.
- Import your newly created bot file.
- Initialize the bot and set up any necessary middleware or error handling.
- Copy an existing function for bot interaction, modify it for the new bot, and ensure it correctly handles the bot’s activities.
- Add a new route to the `init` function for handling requests specific to your bot.

## Submitting Changes

Once you have completed the setup and testing:

- Push your changes to your fork of the repository.
- Submit a pull request against our main branch.
- Provide a detailed description of what your bot does and any other relevant information that will help the reviewers.

## Final Notes

- Ensure your code adheres to the coding standards and practices already in place in the repository.
- Update any documentation relevant to your bot's functionality.

Thank you for contributing to our project! We look forward to reviewing your innovative bot implementations.
