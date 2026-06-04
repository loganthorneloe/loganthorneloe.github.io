#!/usr/bin/env python3
"""
Logan Thorneloe's Personal Site Static Generator
Fetches Substack JSON archive API and GitHub API to build index.html, projects.html, and blog.html.
"""

import os
import json
import urllib.request
import datetime
import re

SUBSTACK_JSON_BASE_URL = "https://aiforswes.com/api/v1/archive?limit=20"
GITHUB_REPOS = [
    "loganthorneloe/ml-roadmap",
    "loganthorneloe/swsh-pokemon-breeder"
]
CACHE_FILE = "cache.json"

# Key articles to feature on the blog page
FEATURED_POST_SLUGS = [
    "machine-learning-infra",
    "the-real-way-to-make-agentic-development"
]

# Manual projects (incorporating the newsletter) with visual assets
MANUAL_PROJECTS = [
    {
        "name": "AI for Software Engineers",
        "description": "A technical newsletter read by over 13,000 software engineers, covering the systems, architecture, and infrastructure behind modern production AI.",
        "custom_stat": "13,000+ subscribers",
        "html_url": "https://aiforswes.com",
        "image_url": "https://substackcdn.com/image/fetch/w_256,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F656213f4-4ebe-4864-9979-a2b65a21f3e3%2Fapple-touch-icon-1024x1024.png"
    }
]

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load cache: {e}")
    return {"posts": [], "projects": {}}

def save_cache(cache_data):
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump(cache_data, f, indent=2)
    except Exception as e:
        print(f"Warning: Failed to save cache: {e}")

def clean_desc(desc):
    if not desc:
        return ""
    # Strip HTML tags
    clean = re.sub(r'<[^>]+>', '', desc)
    # Decode common HTML entities
    clean = clean.replace('&nbsp;', ' ').replace('&#8217;', "'").replace('&#8216;', "'")
    clean = clean.replace('&#8220;', '"').replace('&#8221;', '"').replace('&#8212;', '—')
    clean = clean.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    # Truncate to reasonable length
    if len(clean) > 160:
        return clean[:157].strip() + "..."
    return clean.strip()

def fetch_substack_posts(base_url):
    import time
    posts = []
    # Fetch 5 pages of 20 posts to cover the top 100 posts and older highly liked articles
    for offset in range(0, 100, 20):
        url = f"{base_url}&offset={offset}"
        print(f"Fetching Substack posts offset {offset} via JSON API...")
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
            if not data:
                break
            
            for item in data:
                title = item.get('title', '')
                link = item.get('canonical_url', '')
                post_date_raw = item.get('post_date', '')
                description = item.get('description', '')
                image_url = item.get('cover_image', '')
                reaction_count = item.get('reaction_count', 0)
                comment_count = item.get('comment_count', 0)
                
                # Format date: "2026-05-26T14:03:40.450Z" -> "May 26, 2026"
                pub_date = post_date_raw
                try:
                    date_str = post_date_raw.split(".")[0].replace("Z", "")
                    dt = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
                    pub_date = dt.strftime("%b %d, %Y")
                except Exception:
                    pass
                    
                posts.append({
                    "title": title,
                    "link": link,
                    "pub_date": pub_date,
                    "description": description,
                    "image_url": image_url,
                    "reaction_count": reaction_count,
                    "comment_count": comment_count
                })
            # Brief sleep to avoid hammer warning
            time.sleep(0.2)
        except Exception as e:
            print(f"Error fetching Substack JSON API at offset {offset}: {e}")
            break
            
    return posts if posts else None

def fetch_github_project(repo):
    print(f"Fetching GitHub repo stats for {repo}...")
    url = f"https://api.github.com/repos/{repo}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
        return {
            "name": data.get("name", repo.split("/")[-1]),
            "description": data.get("description", ""),
            "stars": data.get("stargazers_count", 0),
            "forks": data.get("forks_count", 0),
            "html_url": data.get("html_url", f"https://github.com/{repo}")
        }
    except Exception as e:
        print(f"Error fetching GitHub repo {repo}: {e}")
        return None

def render_post_card(post, has_image=True):
    img_tag = ""
    has_image_class = ""
    if has_image and post.get("image_url"):
        img_tag = f'<img class="blog-card-image" src="{post["image_url"]}" alt="{post["title"]}" loading="lazy">'
        has_image_class = "has-image"
    
    desc = clean_desc(post.get("description", ""))
    reaction_count = post.get("reaction_count", 0)
    comment_count = post.get("comment_count", 0)
    
    return f"""
    <a href="{post["link"]}" target="_blank" rel="noopener noreferrer" class="card blog-card {has_image_class}">
      {img_tag}
      <div class="blog-card-content">
        <h3 class="card-title">{post["title"]}</h3>
        <p class="card-desc">{desc}</p>
        <div class="card-meta">
          <div class="card-stats">
            <div class="stat-item" title="Publication Date">
              <span>{post["pub_date"]}</span>
            </div>
            <div style="width: 1px; height: 10px; background-color: var(--border-color); margin: 0 4px;"></div>
            <div class="stat-item" title="Likes">
              <svg class="heart-icon" width="12" height="12" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
              <span>{reaction_count}</span>
            </div>
            <div class="stat-item" title="Comments">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
              <span>{comment_count}</span>
            </div>
          </div>
          <span>Read &rarr;</span>
        </div>
      </div>
    </a>"""

def render_project_card(proj):
    img_tag = ""
    has_image_class = ""
    if proj.get("image_url"):
        img_tag = f'<img class="project-card-image" src="{proj["image_url"]}" alt="{proj["name"]}" loading="lazy">'
        has_image_class = "has-image"

    # Check if this is a manual project with custom stats
    if "custom_stat" in proj:
        stat_block = f"""
          <div class="stat-item">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
            <span>{proj["custom_stat"]}</span>
          </div>"""
        link_label = "Subscribe"
    else:
        stat_block = f"""
          <div class="stat-item">
            <svg class="star-icon" width="14" height="14" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            <span>{proj["stars"]}</span>
          </div>
          <div class="stat-item">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="6" y1="3" x2="6" y2="15"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/></svg>
            <span>{proj["forks"]}</span>
          </div>"""
        link_label = "GitHub"

    return f"""
    <a href="{proj["html_url"]}" target="_blank" rel="noopener noreferrer" class="card project-card {has_image_class}">
      {img_tag}
      <div class="blog-card-content">
        <h3 class="card-title">{proj["name"]}</h3>
        <p class="card-desc">{proj["description"]}</p>
        <div class="card-meta">
          <div class="card-stats">
            {stat_block}
          </div>
        </div>
      </div>
    </a>"""

def build_page(page_name, title, description, content_html):
    # Read base template
    with open("templates/base.html", "r") as f:
        base_html = f.read()
    
    # Replace navigation active classes
    base_html = base_html.replace("{% if active_page == 'about' %}active{% endif %}", "active" if page_name == "about" else "")
    base_html = base_html.replace("{% if active_page == 'projects' %}active{% endif %}", "active" if page_name == "projects" else "")
    base_html = base_html.replace("{% if active_page == 'blog' %}active{% endif %}", "active" if page_name == "blog" else "")
    
    # Replace placeholders
    page_html = base_html.replace("{{ title }}", title)
    page_html = page_html.replace("{{ description }}", description)
    page_html = page_html.replace("{{ content }}", content_html)
    
    # Output file
    output_filename = "index.html" if page_name == "about" else f"{page_name}.html"
    with open(output_filename, "w") as f:
        f.write(page_html)
    print(f"Successfully generated {output_filename}")

def main():
    cache = load_cache()
    
    # 1. Fetch Substack newsletter feed via JSON API
    posts = fetch_substack_posts(SUBSTACK_JSON_BASE_URL)
    if posts:
        cache["posts"] = posts
    else:
        posts = cache.get("posts", [])
        print("Using cached Substack posts.")
        
    # 2. Compile projects list (incorporating manual project)
    projects = []
    for p in MANUAL_PROJECTS:
        projects.append(p)
        
    for repo in GITHUB_REPOS:
        proj_data = fetch_github_project(repo)
        if proj_data:
            # Map visual asset URLs dynamically to GitHub Open Graph previews
            proj_data["image_url"] = f"https://opengraph.githubassets.com/1/{repo}"
                
            cache["projects"][repo] = proj_data
            projects.append(proj_data)
        else:
            cached_proj = cache.get("projects", {}).get(repo)
            if cached_proj:
                cached_proj["image_url"] = f"https://opengraph.githubassets.com/1/{repo}"
                projects.append(cached_proj)
                print(f"Using cached stats for {repo}.")
            else:
                projects.append({
                    "name": repo.split("/")[-1],
                    "description": "Open source repository maintained by Logan Thorneloe.",
                    "stars": 0,
                    "forks": 0,
                    "html_url": f"https://github.com/{repo}"
                })
                
    save_cache(cache)
    
    # Ensure build output matches template configs
    if not posts:
        print("Warning: No blog posts available to render.")
    if not projects:
        print("Warning: No projects available to render.")
        
    # 3. Render and compile pages
    
    # Homepage / About (index.html)
    with open("templates/about.html", "r") as f:
        about_template = f.read()
    
    build_page(
        page_name="about",
        title="About",
        description="Logan Thorneloe - ML Infrastructure & Agents Engineer at Google.",
        content_html=about_template
    )
    
    # Projects Page (projects.html)
    with open("templates/projects.html", "r") as f:
        projects_template = f.read()
        
    projects_list_html = "\n".join(render_project_card(p) for p in projects)
    projects_content = projects_template.replace("{{ projects_list }}", projects_list_html)
    
    build_page(
        page_name="projects",
        title="Projects",
        description="Open source projects and development libraries built by Logan Thorneloe.",
        content_html=projects_content
    )
    
    # Blog Page (blog.html)
    with open("templates/blog.html", "r") as f:
        blog_template = f.read()
        
    featured_posts_html = ""
    blog_list_html = ""
    
    if posts:
        # Match featured articles by their URL slugs
        featured = [p for p in posts if any(slug in p["link"] for slug in FEATURED_POST_SLUGS)]
        # Fallback to the first 2 posts if none match
        if not featured:
            featured = posts[:2]
            
        remaining = [p for p in posts if p not in featured]
        
        featured_posts_html = "\n".join(render_post_card(p, has_image=True) for p in featured)
        # Limit previous articles section to 5 posts
        blog_list_html = "\n".join(render_post_card(p, has_image=True) for p in remaining[:5])
        
    blog_content = blog_template.replace("{{ featured_posts }}", featured_posts_html)
    blog_content = blog_content.replace("{{ blog_list }}", blog_list_html)
    
    build_page(
        page_name="blog",
        title="Blog",
        description="Read the latest articles from AI for Software Engineers by Logan Thorneloe.",
        content_html=blog_content
    )

if __name__ == "__main__":
    main()
