# Stock Notifier Landing Page

This directory contains the landing page for the Stock Notifier project, designed to be hosted on GitHub Pages.

## Features

- **Modern Design**: Clean, professional layout with Bitwarden-inspired dark mode theme
- **Responsive**: Fully responsive design that works on all devices
- **Interactive**: Smooth scrolling, tab switching, and copy-to-clipboard functionality
- **Informative**: Comprehensive sections covering features, how it works, quick start, and compliance

## Sections

1. **Hero Section**: Eye-catching headline with clear call-to-action
2. **Features**: Six key features with icons and descriptions
3. **How It Works**: Step-by-step workflow visualization
4. **Quick Start**: Installation instructions for both Docker and local setup
5. **Compliance Notice**: Important legal disclaimers
6. **Footer**: Links to GitHub repo and documentation

## Hosting on GitHub Pages

### Option 1: GitHub Pages from main branch (Recommended)

1. Go to your repository settings on GitHub
2. Navigate to **Settings** > **Pages**
3. Under **Source**, select **Deploy from a branch**
4. Select the **master** (or **main**) branch
5. Select the **/ (root)** folder and click **Save**
6. Copy the `landing-page` directory contents to the root of your repository, or...
7. Move the landing-page files to a `docs` folder and select **/docs** as the source

### Option 2: GitHub Pages from docs folder

1. Create a `docs` folder in the root of your repository:
   ```bash
   mkdir docs
   cp -r landing-page/* docs/
   ```

2. Commit and push:
   ```bash
   git add docs/
   git commit -m "Add landing page to docs folder"
   git push
   ```

3. In GitHub repository settings:
   - Go to **Settings** > **Pages**
   - Select **master** branch and **/docs** folder
   - Click **Save**

4. Your site will be available at: `https://IbyG.github.io/Stock-Notifier/`

### Option 3: Separate gh-pages branch

1. Create and checkout a new `gh-pages` branch:
   ```bash
   git checkout --orphan gh-pages
   ```

2. Remove all files except the landing page:
   ```bash
   git rm -rf .
   cp -r landing-page/* .
   rm -rf landing-page
   ```

3. Commit and push:
   ```bash
   git add .
   git commit -m "Initial landing page commit"
   git push origin gh-pages
   ```

4. In GitHub repository settings:
   - Go to **Settings** > **Pages**
   - Select **gh-pages** branch
   - Click **Save**

5. Your site will be available at: `https://yourusername.github.io/Stock-Notifier/`

## Local Development

To test the landing page locally:

1. Navigate to the landing-page directory:
   ```bash
   cd landing-page
   ```

2. Start a local server (choose one):
   
   **Using Python:**
   ```bash
   python -m http.server 8000
   ```
   
   **Using Node.js:**
   ```bash
   npx serve
   ```
   
   **Using PHP:**
   ```bash
   php -S localhost:8000
   ```

3. Open your browser to `http://localhost:8000`

## Customization

### Colors

The color theme is defined in CSS variables at the top of `styles.css`. To customize:

```css
:root {
    --bg-primary: #1c2130;        /* Main background */
    --accent-primary: #175ddc;    /* Primary accent color */
    /* ... other colors ... */
}
```

### Content

Edit `index.html` to modify:
- Text content
- Links to your repository
- Contact information
- Features and descriptions

### Fonts

The landing page uses the Inter font from Google Fonts. To change it, modify the link in `index.html` and the CSS in `styles.css`.

## Files

- `index.html` - Main HTML structure
- `styles.css` - All styling and layout
- `script.js` - Interactive functionality
- `README.md` - This file

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers

## License

Same as the main Stock Notifier project.

