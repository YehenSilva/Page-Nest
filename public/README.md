# PageNest 🚀 — Advanced Notes & Knowledge Sharing Workspace

**PageNest** is an advanced, collaborative knowledge base and notes sharing system built directly into a lightweight single-page application (`index.html`). Designed to run 100% on Firebase's free (Spark) plan without paid storage buckets.

---

## ✨ Features & Capabilities

- 🎨 **Modern Design System & Branding**: Custom vector SVG logo, SVG favicon, light/dark themes, clean typography, smooth transitions, and responsive mobile drawer.
- 🖼️ **Cover Images & Icons**: Add aesthetic gradient banners (8 curated presets or custom image URLs) and categorized emoji icons to any document.
- ⚡ **Global Search & Command Palette (`Ctrl + K`)**: Instant modal search across all document titles and body contents with keyboard navigation.
- 📂 **Focus Mode & Sidebar Collapse (`Ctrl + \`)**: Hide or expand the sidebar for a distraction-free writing canvas.
- 📝 **Rich Block Editor**:
  - Headings (H1, H2, H3) with markdown triggers (`#`, `##`, `###`).
  - Bulleted and numbered lists with indent/outdent (`Tab` / `Shift + Tab`).
  - Interactive to-do checklists with smooth completion animation.
  - Collapsible toggle lists (`▸`).
  - Stylized callout cards with selectable icons.
  - Formatted quotes, dividers, and sub-page cards.
  - Syntax code blocks with language indicators and one-click copy.
  - Interactive data tables with `Tab` cell navigation, row/column tools, and CSV/Excel import & export.
- 📎 **Zero-Storage-Cost File Engine**:
  - Upload PDFs, Word documents (`.docx`), Excel spreadsheets (`.xlsx`, `.xls`, `.csv`), images, audio, and video.
  - Stored inside Firestore chunks — zero Google Cloud Storage fees.
  - In-page preview for PDF, DOCX (Mammoth), XLSX (SheetJS tabs), and text.
  - Full-screen image lightbox zoom.
- 👥 **Advanced Sharing System**:
  - **Share to Web**: Instant public link generation for read-only guest viewing without requiring login.
  - **Collaborator Invitations**: Invite registered users by email with specific roles (*Can edit* or *Can view*).
  - Member management roster to adjust roles or revoke access.
- 📤 **Multi-Format Exports**:
  - Export to Markdown (`.md`).
  - Export to Standalone HTML (`.html`) with embedded styles.
  - Print / Save as PDF with clean document print styles.

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
| :--- | :--- |
| `Ctrl + K` / `Cmd + K` | Open global search & command palette |
| `Ctrl + \` / `Cmd + \` | Toggle sidebar (Focus mode) |
| `Ctrl + S` / `Cmd + S` | Force instant save |
| `Alt + N` | Create a new page |
| `/` (on empty line) | Open block command menu |
| `Tab` / `Shift + Tab` | Indent / outdent list item, or navigate table cells |
| `Enter` (in table) | Move to cell below or create new row at bottom |
| `#`, `##`, `###` + `Space` | Create Heading 1, 2, or 3 |
| `[]` + `Space` | Create to-do checklist item |
| `-` or `*` + `Space` | Create bulleted list item |
| `1.` + `Space` | Create numbered list item |
| `>` + `Space` | Create quote block |
| `---` + `Enter` | Create divider |
| ` ``` ` + `Enter` | Create code snippet |

---

## 🚀 Setup & Deployment

1. **Firebase Project**:
   - `console.firebase.google.com` → **Add project** → **Add app → Web**.
   - Copy the configuration object into `firebaseConfig` in `public/index.html`.
2. **Authentication**:
   - **Build → Authentication → Sign-in method**: enable **Email/Password** and **Google**.
   - **Settings → Authorized domains**: add your custom domain or deployment URL.
3. **Firestore Security Rules**:
   - Deploy `firestore.rules` using the Firebase CLI or paste into the Firestore Console rules tab.
4. **Deploy**:
   - Deploy with Firebase Hosting (`firebase deploy --only hosting`), Vercel, Netlify, or any static web server.
