# Landing Page Deployment Guide

This guide provides step-by-step instructions for deploying the Stock Notifier landing page to various hosting platforms.

## Table of Contents

1. [GitHub Pages (Recommended)](#github-pages-recommended)
2. [Netlify](#netlify)
3. [Vercel](#vercel)
4. [Custom Domain Setup](#custom-domain-setup)

---

## GitHub Pages (Recommended)

GitHub Pages is the easiest way to host static sites directly from your GitHub repository.

### Method 1: Deploy from docs folder

This is the recommended method as it keeps the landing page separate from the main codebase.

1. **Create docs folder and copy files:**
   ```bash
   mkdir docs
   cp -r landing-page/* docs/
   git add docs/
   git commit -m "Add landing page for GitHub Pages"
   git push origin master
   ```

2. **Enable GitHub Pages:**
   - Go to your repository on GitHub
   - Click **Settings** > **Pages**
   - Under **Source**, select **Deploy from a branch**
   - Choose **master** branch and **/docs** folder
   - Click **Save**

3. **Access your site:**
   - Your landing page will be available at: `https://IbyG.github.io/Stock-Notifier/`
   - It may take a few minutes for the site to go live

### Method 2: Deploy from gh-pages branch

This method uses a separate branch dedicated to the landing page.

1. **Create gh-pages branch:**
   ```bash
   git checkout --orphan gh-pages
   git rm -rf .
   ```

2. **Copy landing page files:**
   ```bash
   cp -r landing-page/* .
   rm -rf landing-page
   ```

3. **Commit and push:**
   ```bash
   git add .
   git commit -m "Initial landing page deployment"
   git push origin gh-pages
   ```

4. **Configure GitHub Pages:**
   - Go to **Settings** > **Pages**
   - Select **gh-pages** branch as source
   - Click **Save**

5. **Return to main branch:**
   ```bash
   git checkout master
   ```

### Troubleshooting GitHub Pages

- **404 Error**: Ensure the branch and folder are correctly selected in settings
- **Assets not loading**: Check that all file paths are relative, not absolute
- **Changes not showing**: It can take 5-10 minutes for changes to deploy
- **Custom styling issues**: The `.nojekyll` file prevents Jekyll processing (already included)

---

## Netlify

Netlify offers free hosting with automatic deployments and custom domains.

### Deploy to Netlify

1. **Sign up for Netlify:**
   - Go to [netlify.com](https://www.netlify.com)
   - Sign up with your GitHub account

2. **Create new site:**
   - Click **Add new site** > **Import an existing project**
   - Connect to your GitHub repository
   - Select your Stock-Notifier repository

3. **Configure build settings:**
   - **Base directory**: `landing-page`
   - **Build command**: (leave empty)
   - **Publish directory**: `landing-page`
   - Click **Deploy site**

4. **Your site is live:**
   - Netlify will provide a URL like `random-name-123456.netlify.app`
   - You can customize this in **Site settings** > **Change site name**

### Continuous Deployment

Netlify automatically redeploys your site when you push to the master branch. No additional configuration needed!

---

## Vercel

Vercel provides fast, global hosting for static sites with excellent performance.

### Deploy to Vercel

1. **Sign up for Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Sign up with your GitHub account

2. **Import project:**
   - Click **Add New** > **Project**
   - Import your Stock-Notifier repository

3. **Configure project:**
   - **Framework Preset**: Other
   - **Root Directory**: `landing-page`
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)
   - Click **Deploy**

4. **Access your site:**
   - Vercel provides a URL like `stock-notifier.vercel.app`
   - Automatic HTTPS is included

---

## Custom Domain Setup

Once your site is deployed, you can add a custom domain.

### GitHub Pages Custom Domain

1. **Purchase a domain** from a registrar (Namecheap, GoDaddy, etc.)

2. **Create CNAME file:**
   ```bash
   echo "yourdomain.com" > landing-page/CNAME
   git add landing-page/CNAME
   git commit -m "Add custom domain"
   git push
   ```

3. **Configure DNS:**
   Add the following DNS records at your domain registrar:
   
   **For apex domain (yourdomain.com):**
   ```
   Type: A
   Name: @
   Value: 185.199.108.153
   
   Type: A
   Name: @
   Value: 185.199.109.153
   
   Type: A
   Name: @
   Value: 185.199.110.153
   
   Type: A
   Name: @
   Value: 185.199.111.153
   ```
   
   **For subdomain (www.yourdomain.com):**
   ```
   Type: CNAME
   Name: www
   Value: IbyG.github.io
   ```

4. **Enable HTTPS:**
   - Go to **Settings** > **Pages**
   - Check **Enforce HTTPS**

### Netlify Custom Domain

1. **Add custom domain:**
   - Go to **Site settings** > **Domain management**
   - Click **Add custom domain**
   - Enter your domain name

2. **Configure DNS:**
   - Netlify will provide DNS instructions
   - Either use Netlify DNS (recommended) or configure your registrar's DNS

3. **HTTPS is automatic** with Netlify

### Vercel Custom Domain

1. **Add domain:**
   - Go to **Project Settings** > **Domains**
   - Enter your domain name

2. **Configure DNS:**
   - Vercel will show the DNS records to add
   - Add them at your domain registrar

3. **HTTPS is automatic** with Vercel

---

## Performance Optimization

### Enable Caching

All platforms handle caching automatically, but you can improve it:

- **GitHub Pages**: Caching is handled automatically
- **Netlify**: Configure in `netlify.toml` (optional)
- **Vercel**: Configure in `vercel.json` (optional)

### Compress Images

If you add images to the landing page:

```bash
# Using imagemagick
convert input.png -quality 85 output.png

# Using online tools
https://tinypng.com
https://squoosh.app
```

### Minify Assets

For production, consider minifying CSS/JS:

```bash
# Using online tools
https://cssminifier.com
https://javascript-minifier.com
```

---

## Monitoring and Analytics

### Google Analytics

Add to the `<head>` section in `index.html`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Simple Analytics (Privacy-Friendly)

```html
<script async defer src="https://scripts.simpleanalyticscdn.com/latest.js"></script>
<noscript><img src="https://queue.simpleanalyticscdn.com/noscript.gif" alt="" referrerpolicy="no-referrer-when-downgrade" /></noscript>
```

---

## Updating the Landing Page

### For GitHub Pages

```bash
# Make changes to landing-page files
git add landing-page/
git commit -m "Update landing page"
git push

# If using docs folder, copy changes:
cp -r landing-page/* docs/
git add docs/
git commit -m "Update landing page"
git push
```

### For Netlify/Vercel

Simply push to your GitHub repository. Automatic deployment handles the rest!

---

## Support

If you encounter issues:

1. Check the platform's documentation
2. Review deployment logs
3. Verify all file paths are relative
4. Ensure `.nojekyll` file exists for GitHub Pages
5. Open an issue on the GitHub repository

---

## Additional Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Netlify Documentation](https://docs.netlify.com)
- [Vercel Documentation](https://vercel.com/docs)
- [Custom Domain Setup Guide](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)

