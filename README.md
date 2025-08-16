# Crowdfunding Back End
{{ your name here }}

## Planning:
### Concept/Name
{{ Include a short description of your website concept here. }}

### Intended Audience/User Stories
{{ Who are your intended audience? How will they use the website? }}

### Front End Pages/Functionality
- Home Page
   - Featured fundraiser
- Search page
   - Search specific fundraiser
- Create New Fundraiser Page
   - Form with fundraiser details 
   - Ability to submit
   - Nice error handling
- Display fundraiser
   - Shows all information  

### API Spec
{{ Fill out the table below to define your endpoints. An example of what this might look like is shown at the bottom of the page. 

It might look messy here in the PDF, but once it's rendered it looks very neat! 

It can be helpful to keep the markdown preview open in VS Code so that you can see what you're typing more easily. }}

| URL          | Purpose                   | HTTP         | Request Body | Success Response Code | Authentication/Authorisation |
| ------------ | ------------------------- | ------------ | ------------ | --------------------- | ---------------------------- |
| /fundraisers | Fetch all the fundraisers | GET          | N/A          | 200                   | none                         |
| /fundraisers | Create a new fundraiser   | POST         | JSON Payload | 201                   | Any logged in user           |
| /pledges/    | Fetch all the pledges.    | GET          | N/A          | 200                   |                              |
| pledges      | create a new pledge       | JSON Payload | 201          | Any logged in user    |
### DB Schema
![]( {{ ./relative/path/to/your/schema/image.png }} )