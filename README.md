# Crowdfunding Back End
Emma Spear

## Planning:
### Concept/Name
**PokePledge** is a crowdfunding app with a Pokémon twist. 
Trainers can create fundraisers on behalf of their Pokémon — like Snorlax asking for a beanbag chair or Eevee hoping for grooming supplies — and the community can pledge support to bring those wishes to life.  

The project demonstrates a full-stack Django REST Framework + React build, with user accounts, fundraisers, and pledges.

### Intended Audience/User Stories
The intended audience includes:
- **Pokémon trainers** who want to create fun fundraisers on behalf of their Pokémon.  
- **Supporters** who enjoy pledging to bring those Pokémon dreams to reality.  

User stories:
- As a trainer, I can create an account so that I can manage my fundraisers.  
- As a trainer, I can create a fundraiser with a title, description, and goal amount so my Pokémon’s wish can be shared.  
- As a supporter, I can browse available fundraisers and pledge to ones that interest me.  
- As a trainer, I can see pledges made to my fundraiser.  
- As a logged-in user, I can only edit or delete fundraisers/pledges that I own.  

### Front End Pages/Functionality
- **Home Page**
  - Lists all active fundraisers  
  - Search and filter options  
  - Links to fundraiser details  

- **Fundraiser Detail Page**
  - Displays fundraiser description, goal, progress, and pledges  
  - Shows trainer info  
  - “Pledge” form for logged-in users  

- **User Account Pages**
  - Signup / Login / Logout  
  - Dashboard showing user’s fundraisers and pledges  

- **Create/Edit Fundraiser Page**
  - Form to create new fundraisers (title, description, goal, Pokémon wish)  
  - Ability to edit or delete fundraisers you own  

### API Spec


| URL                   | HTTP Method | Purpose                     | Request Body  | Success Response Code | Authentication/Authorisation |
| --------------------- | ----------- | --------------------------- | ------------- | --------------------- | ---------------------------- |
| /fundraisers/         | GET         | Fetch all the fundraisers   | N/A           | 200                   | None                         |
| /fundraisers/         | POST        | Create a new fundraiser     | JSON Payload  | 201                   | Any logged in user           |
| /fundraisers/id/      | GET         | Fetch a single fundraiser   | N/A           | 200                   | None                         |
| /fundraisers/?/       | PUT/PATCH   | Update fundraiser           |               | 200                   | Owner only                   |
| /fundraisers/         | DELETE      | Delete fundraiser           |               | 204                   | Owner only                   |
| /pledges/             | GET         | Fetch pledges               | N/A           | 200                   | None                         |
| /pledges              | POST        | Create a new pledge         | JSON Payload  | 201                   | Any logged in user           |
| /users/new            | POST        | Register new user           | JSON Payload  | 201                   | None                         |
| /users/login          | POST        | Authenticate and login user | JSON Payload  | 200                   | None                         |
| /users/profile/       | GET         | View user's profile         |               | 200                   | User only                    |
| /users/account        | GET         | View users account          |               |                       | User only                    |
| /users/account/edit   | POST        | Edit account                | JASON Payload |                       | Owner only                   |
| /users/account/delete | DELETE      | Delete account              |               |                       | Owner only                   |
| /users/account/logout | POST        | Logout                      | POST          |                       | User only                    |
### DB Schema
![]( {{ ./relative/path/to/your/schema/image.png }} )