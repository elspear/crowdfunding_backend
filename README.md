# Crowdfunding Back End
Emma Spear

## Planning:
### Concept/Name
**PokePledge** is a crowdfunding app with a Pokémon twist. 
Trainers can create fundraisers on behalf of their Pokémon — like Snorlax asking for a beanbag chair or Eevee hoping for grooming supplies — and the community can pledge support to bring those wishes to life.  

The project demonstrates a full-stack Django REST Framework + React build, with user accounts, fundraisers, and pledges.

### Intended Audience/User Stories
The intended audience includes:
- **Pokémon trainers** who want to create fundraisers on behalf of their Pokémon. 
- **Pokémon Centers** who want to create fundraisers to benefit the community.
- **Safari Parks** who want to create fundraisers to raise money for Pokémon welfare. 
- **Supporters** who enjoy pledging to bring those Pokémon dreams to reality.  

**User stories:**
Accounts & Roles
- As a new user, I can sign up with a username, email, and password.
- As a user, I can log in and receive a token so I can make authenticated requests.
- As a user, I can choose my role (trainer, Pokémon Center admin, Safari Park admin) at signup.
- As user, I can update my account information as well as delete my account. 

Create & Manage Fundraisers
- As a trainer, I can create a fundraiser with a title, description, goal (₽), Pokémon name, image and items needed.
- As a Pokémon Center admin, I can create a welfare fundraiser (e.g., relocations, medical needs) so that the community can back local projects.
- As a Safari Park admin, I can create a conservation fundraiser so supporters can fund endangered Pokémon.
- As a fundraiser owner, I can edit or delete my own fundraiser.

Discover & Pledge
- As a supporter (any logged-in user), I can browse all fundraisers and view details so I can decide where to pledge.
- As a supporter, I can create a pledge on a fundraiser (₽ amount and comment) to contribute, with the option to remain anonymous or not.
- As a supporter, I can edit or delete my own pledge.

Visibility & Safety
- As a fundraiser owner, I can see pledges to my fundraiser so I can track progress
- As a logged-in user, I can only edit or delete resources I own (fundraisers and/or pledges).


### Front End Pages/Functionality
- **Home Page**
  - Featured fundraisers.
  - Search and filter options.  
  - Logged-in user's can track progress on fundraiser's they have pledged to. 

- **Fundraiser Detail Page**
  - Displays fundraiser description, goal, progress, and pledges.  
  - Shows trainer info as well as progress to the fundraiser's goal. 
  - “Pledge” form for logged-in users.  

- **User Account Pages**
  - Signup, log in, log out. 
  - Update account details or delete account
  - View own fundraisers and pledges. 

- **Create/Edit Fundraiser Page**
  - Form to create new fundraisers
  - Ability to edit or delete fundraisers you own  

### API Spec


| URL                | HTTP Method | Purpose                     | Request Body | Success Response Code | Authentication/Authorisation |
| ------------------ | ----------- | --------------------------- | ------------ | --------------------- | ---------------------------- |
| /fundraisers/      | GET         | Fetch all the fundraisers   | N/A          | 200                   | None                         |
| /fundraisers/      | POST        | Create a new fundraiser     | JSON Payload | 201                   | Any logged in user           |
| /fundraisers/<id>/ | GET         | Fetch a single fundraiser   | N/A          | 200                   | None                         |
| /fundraisers/<id>/ | PUT         | Update fundraiser           | JSON Payload | 200                   | Fundraiser owner             |
| /fundraisers/<id>/ | DELETE      | Delete fundraiser           | N/A          | 204                   | Fundraiser owner             |
| /pledges/          | GET         | Fetch pledges               | N/A          | 200                   | None                         |
| /pledges/<id>/     | GET         | Fetch a single pledge       | N/A          | 200                   | None                         |
| /pledges/          | POST        | Create a new pledge         | JSON Payload | 201                   | Any logged in user           |
| /pledges/<id>/     | PUT         | Update a pledge             | JSON Payload | 200                   | Pledge owner                 |
| /users/            | POST        | Register new user           | JSON Payload | 201                   | None                         |
| /users/            | POST        | Authenticate and login user | JSON Payload | 200                   | None                         |
| /users/            | PUT         | Edit account                | JSON Payload | 200                   | Account owner                |
| /users/            | DELETE      | Delete account              | N/A          |                       | Account owner                |
### DB Schema
![Database Schema](database.drawio.svg)