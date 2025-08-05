# My Academic Personal Website

This repository contains the source code for a my academic website, built with [Hugo](https://gohugo.io/) and deployed on GitHub Pages.

## Project Structure

```
├── archetypes/          # Content templates
├── assets/              # Theme assets (CSS, JS)
├── content/             # Main content
│   ├── _index.md        # Homepage content
│   ├── cv/              # CV page
│   ├── posts/           # Blog posts
│   └── publications/    # Publications page
├── data/
│   └── publications.yaml # Publications data
├── layouts/             # Custom layout templates
├── static/              # Static assets (images, PDFs, etc.)
├── themes/gokarna/      # Hugo theme
├── hugo.toml           # Hugo configuration
└── public/             # Generated static site (auto-generated)
```

## Setup and Development

### Prerequisites

- [Hugo](https://gohugo.io/installation/) (extended version recommended)
- [Git](https://git-scm.com/)

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/your-academic-website.git
   cd your-academic-website
   ```

2. **Initialize the theme submodule** (if not already done):
   ```bash
   git submodule update --init --recursive
   ```

3. **Start the development server**:
   ```bash
   hugo server -D
   ```

4. **View the site**: Open [http://localhost:1313](http://localhost:1313) in your browser

### Building for Production

```bash
hugo --minify
```

The generated static files will be in the `public/` directory.

## Content Management

### Adding Publications

Publications are managed in `data/publications.yaml`. Add new entries following this format:

```yaml
2025:
  - title: "Your Paper Title"
    authors: "Author Names"
    venue: "Full Conference/Journal Name"
    venue_short: "SHORT NAME"
    year: 2025
    pdf: "https://link-to-pdf.com"
    code: "https://github.com/repo"  # or null if no code
```

### Adding Blog Posts

Create new posts in the `content/posts/` directory:

```bash
hugo new posts/your-post-title.md
```

### Updating CV

- Update the content in `content/cv/_index.md`
- Replace the PDF file in `static/pdf/CV.pdf`

### Adding Images

Place images in `static/images/` and reference them in content as `/images/filename.jpg`

## Configuration

Key configuration options in `hugo.toml`:

- **Site Information**: Update `title`, `baseURL`, and `description`
- **Social Links**: Modify the `socialIcons` array to include your academic profiles
- **Navigation**: Edit the `menu.main` sections
- **Analytics**: Update analytics tracking script in `customHeadHTML` if desired

## Deployment

The site is automatically deployed to GitHub Pages when changes are pushed to the `main` branch. The deployment workflow uses GitHub Actions.

### Manual Deployment

If you need to deploy manually:

1. Build the site: `hugo --minify`
2. The `public/` directory contains the deployable files
3. Deploy the contents of `public/` to your hosting service

## Analytics

The site supports privacy-focused analytics. The tracking script can be configured in the `customHeadHTML` section of `hugo.toml`.

## License

This project is open source. The content is personal academic work, while the theme is licensed under its respective license.

## Customization

To customize this template for your own use:

1. Update `hugo.toml` with your site information
2. Replace content in `content/_index.md` with your bio
3. Update `data/publications.yaml` with your publications
4. Replace images in `static/images/` with your photos
5. Update CV content and PDF in the respective directories
6. Modify social links and contact information

## Acknowledgments

- Built with [Hugo](https://gohugo.io/)
- Theme: [Gokarna](https://github.com/gokarna-theme/gokarna-hugo/) by Yash Mehrotra and Avijit Gupta
- Hosted on [GitHub Pages](https://pages.github.com/)
