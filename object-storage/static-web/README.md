# Static Website Hosting via Object Storage

## 1. Objective

Host a fully static website using S3-compatible object storage without managing servers.

Requirements:

- High availability
- Low operational overhead
- Cost efficiency
- No server-side runtime

---

## 2. Architecture

Object Storage is used as:

- Static file hosting layer
- Website endpoint
- Optional CDN origin

Supported content:

- HTML
- CSS
- JavaScript
- Static assets

Not supported:

- Server-side rendering
- Backend APIs
- Database-driven content

---

## 3. Availability Model

- Built-in redundancy
- No VM management
- Serverless distribution
- Horizontally scalable

---

## 4. DNS Configuration

Bucket name must match domain:

www.example.com

DNS record:

www.example.com CNAME www.example.com.website.yandexcloud.net

Limitation:

- Only third-level domains supported via CNAME
- Apex/root domains require additional DNS or CDN configuration

---

## 5. HTTPS

- HTTP enabled by default
- HTTPS requires TLS certificate configuration
- Recommended to use CDN for managed TLS

---

## 6. Security Model

- Public read-only access
- No anonymous write permissions
- Public access limited to GetObject
- Minimal attack surface

---

## 7. Result

Provides:

- Serverless website hosting
- High availability
- Low cost
- Minimal maintenance
