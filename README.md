# Bookshelf

<div align="center">
<div style="display: flex; gap:.5rem">
<img alt="Static Badge" src="https://img.shields.io/badge/Django-%23092E20?style=flat-square&logo=django">
<img alt="Static Badge" src="https://img.shields.io/badge/Vercel-black?style=flat-square&logo=vercel">
<img alt="Static Badge" src="https://img.shields.io/badge/HTML-%23E34F26?style=flat-square&logo=html5&logoColor=white">
</div>
</div>

## Bookshelf is a full-featured bookshop website built with Django

## Demo

[Live deployment](https://bookshelf-ochre.vercel.app/) (may take several seconds to load on cold start)
[![Main page preview](https://raw.githubusercontent.com/SherlockH0/bookshelf/main/preview.png "Main page preview")](https://bookshelf-ochre.vercel.app/)

## Features

- User authentication system: Users can register, login and update their profile information.
- Wishlist and cart functionality for both authenticated users (stored in the database) and guest users (stored in cookies).
- PayPal Checkout integration: Checkout is available for both guest and registered users, with orders being saved to the database after successful payment.
- Responsive website design.
- In-site search functionality.

## Tech-stack

- **Back-end**
  - [Django](https://www.djangoproject.com/)
  - PostgreSQL (Database)
  - [Cloudinary](https://cloudinary.com/) (Image hosting)
- **Front-end**
  - [PayPal Checkout](https://www.paypal.com/bm/webapps/mpp/paypal-checkout)
  - [Pico CSS ✨](https://picocss.com/)
  - JavaScript
- **Deployment**
  - [Vercel](https://vercel.com/)

## Lessons Learned

This was a really interesting project for me, being my first experience with using cookies, PayPall Checkout and deploing a web application.
