# Crowdfunding Back End
Emma Spear

## Planning:
### Concept/Name
**PokePledge** is a crowdfunding app with a Pokémon twist. 
Trainers can create fundraisers on behalf of their Pokémon — like Snorlax asking for a beanbag chair or Eevee hoping for a special crystal to ✨ evolve ✨ — and the community can pledge support to bring those wishes to life.  

The project demonstrates a full-stack Django REST Framework + React build, with user accounts, fundraisers, pledges, and more.

### Intended Audience/User Stories
The intended audience includes:
- **Pokémon trainers** who want to create fundraisers on behalf of their Pokémon. 
- **Pokémon Centers** who want to create fundraisers to benefit the community.
- **Safari Parks** who want to create fundraisers to raise money for Pokémon welfare. 
- **Supporters** who enjoy pledging to bring those Pokémon dreams to reality.  

**User stories:**
Accounts & Roles
- As a visitor, I can browse open fundraisers.
- As a supporter, I can pledge to fundraisers that interest me, and choose whether my donation is public or anonymous.
- As a user, I can create a profile page.
- As a fundraiser owner, I can update my fundraiser details and close it when the goal is met.

Create & Manage Fundraisers
- Any user role can create a fundraiser with a title, description, goal (₽), Pokémon name, image, and items needed. 
- Fundraisers will show a preview of recent pledges, including username, amount and comment (excluding anonymous pledges)
- As a trainer, I can create a fundraiser for one of my Pokémon. 
- As a Pokémon Center admin, I can create a welfare fundraiser (e.g., relocations, medical needs) so that the community can back local projects.
- As a Safari Park admin, I can create a conservation fundraiser so supporters can fund endangered Pokémon.
- As a fundraiser owner, I can edit or delete my own fundraiser.

Discover & Pledge
- As a supporter (any logged-in user), I can browse all fundraisers and view details so I can decide where to pledge.
- As a supporter, I can create a pledge on a fundraiser (₽ amount and comment) to contribute, with the option to remain anonymous or not.
- As a supporter, I can edit my pledge. (Pledges cannot be deleted, and the amount can only be increased)

Visibility & Safety
- As a fundraiser owner, I can see pledges to my fundraiser so I can track progress
- As a logged-in user, I can only edit or delete resources I own (fundraisers, pledges, profile information).


### Front End Pages/Functionality
- **Home Page**
  - Login or create new user
  - View featured fundraisers
  - Search and filter options for fundraisers

- **Fundraiser Detail Page**
  - Displays fundraiser description, goal, progress, and pledges.  
  - “Pledge” form for logged-in users.  
  - Preview of recent non-anonymous pledges (username, amount, comment)

- **User Account Pages**
  - Signup, log in, log out. 
  - Update account details or delete account.
  - View own fundraisers and their pledges. 
  - View pledges and monitor goal progression on pledged fundraisers.
  - Create, view, and edit own profile.

- **Create/Edit Fundraiser Page**
  - Form to create new fundraisers.
  - Ability to edit or delete fundraisers you own. 

### API Spec


| URL                  | HTTP Method | Purpose                        | Request Body | Success Response Code | Authentication/Authorisation |
| -------------------- | ----------- | ------------------------------ | ------------ | --------------------- | ---------------------------- |
| /fundraisers/        | GET         | Fetch all the fundraisers      | N/A          | 200                   | None                         |
| /fundraisers/        | POST        | Create a new fundraiser        | JSON Payload | 201                   | Any logged in user           |
| /fundraisers/{id}/   | GET         | Fetch a single fundraiser      | N/A          | 200                   | None                         |
| /fundraisers/{id}/   | PUT         | Update fundraiser              | JSON Payload | 200                   | Fundraiser owner             |
| /fundraisers/{id}/   | DELETE      | Delete fundraiser              | N/A          | 204                   | Fundraiser owner             |
| /pledges/            | GET         | Fetch pledges                  | N/A          | 200                   | None                         |
| /pledges/{id}/       | GET         | Fetch a single pledge          | N/A          | 200                   | None                         |
| /pledges/            | POST        | Create a new pledge            | JSON Payload | 201                   | Any logged in user           |
| /pledges/{id}/       | PUT         | Update a pledge                | JSON Payload | 200                   | Pledge owner                 |
| /users/              | POST        | Register new user              | JSON Payload | 201                   | None                         |
| /users/              | POST        | Authenticate and login user    | JSON Payload | 200                   | None                         |
| /users/              | PUT         | Edit account                   | JSON Payload | 200                   | Account owner                |
| /users/              | DELETE      | Delete account                 | N/A          |                       | Account owner                |
| /users/profile/{id}/ | GET         | Fetch a users profile          | N/A          | 200                   | Any logged in user           |
| /users/profile/{id}/ | PATCH         | Fill out / update user profile | JSON Payload | 200                   | Profile owner                |
|/site-stats/ | GET | Fetch site stats on fundraisers | N/A | 
### DB Schema
![Database Schema](database.drawio.svg)

[Heroku Deployment](https://pokepledge-8bbc7b3617c3.herokuapp.com/)

### Creating a New User
To create a new user, a POST request must be sent to the /users/ endpoint with a JSON payload containing the mandatory fields:
- Username
- Email
- Role
- Password
  
![](./images/Post-Create-User.png)

### Creating a New Fundraiser
To create a new fundraiser, a POST request must be sent to the /fundraisers/ endpoint with a JSON payload containing the mandatory fields:
- Title
- Description
- Pokemon
- Goal
- Items Needed (list)
- Image 

![](./images/Post-Create-Fundraiser.png)

## Insomnia Screenshots
### Successful POST method: Create a new pledge
![](./images/Post-Create-Pledge.png)

### Successful GET method: Fetch an individual fundraiser
![](./images/Get-Individual-Fundraiser.png)

### Successful Auth Token
![](./images/Get-Auth-Token.png)
