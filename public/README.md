# Pagenest — setup for the free Firebase (Spark) plan

`index.html` is the whole app. No paid plan and no Firebase Storage needed: uploaded files are stored inside Firestore.

## 1. Firebase project
1. console.firebase.google.com → **Add project** → **Add app → Web**, copy the config.
2. Paste it into `firebaseConfig` near the top of the script in `index.html`.

## 2. Authentication
**Build → Authentication → Sign-in method**: enable **Email/Password** and **Google**.
**Settings → Authorized domains**: add the domain you deploy to (e.g. `yourapp.vercel.app`).

## 3. Firestore
**Build → Firestore Database → Create**, then **Rules** → paste and publish:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    function canReadPage(pid) {
      let p = get(/databases/$(database)/documents/pages/$(pid)).data;
      return p.public == true
        || (request.auth != null && request.auth.uid in p.memberIds);
    }
    function ownsFile(fid) {
      return request.auth != null
        && get(/databases/$(database)/documents/files/$(fid)).data.ownerId == request.auth.uid;
    }

    match /users/{uid} {
      allow read: if request.auth != null;
      allow write: if request.auth.uid == uid;
    }

    match /pages/{id} {
      allow read: if resource.data.public == true
        || (request.auth != null && request.auth.uid in resource.data.memberIds);
      allow create: if request.auth != null
        && request.resource.data.ownerId == request.auth.uid
        && request.auth.uid in request.resource.data.memberIds;
      allow update: if request.auth != null && (
        resource.data.ownerId == request.auth.uid
        || (request.auth.uid in resource.data.editorIds
            && request.resource.data.ownerId == resource.data.ownerId
            && request.resource.data.memberIds == resource.data.memberIds
            && request.resource.data.editorIds == resource.data.editorIds
            && request.resource.data.viewerIds == resource.data.viewerIds
            && request.resource.data.public == resource.data.public));
      allow delete: if request.auth != null && resource.data.ownerId == request.auth.uid;
    }

    match /files/{fid} {
      allow read: if canReadPage(resource.data.pageId);
      allow create: if request.auth != null && request.resource.data.ownerId == request.auth.uid;
      allow delete: if request.auth != null && resource.data.ownerId == request.auth.uid;
      match /chunks/{c} {
        allow read: if canReadPage(get(/databases/$(database)/documents/files/$(fid)).data.pageId);
        allow create, delete: if ownsFile(fid);
      }
    }
  }
}
```

## 4. Deploy
Any static host: Vercel, Netlify, Firebase Hosting — upload `index.html`.

## Free-plan limits to know
- **Files: 5 MB max each.** Photos are auto-compressed (max 1600 px) before upload, so most pictures are well under that.
- Firestore free quota: 1 GiB stored, ~50,000 reads and 20,000 writes per day. Every file view downloads its chunks once per page load (cached while the tab is open), so a handful of users is fine; very heavy use may hit the daily read quota.
- Word/Excel/PDF preview works with no extra setup (files load from the database, so no CORS step).
- Deleting a file block does not erase the stored file data (it can be shared by duplicated blocks). Orphans are small and can be removed from the Firestore console (`files` collection).

## Sharing
- **Share → Invite**: email of someone who has *registered*; *Can edit* or *Can view*. Sub-pages you own are shared too.
- **Share to web**: anyone with the link can read the page without signing in.
- Shared pages show under **Shared with me**.

## Other limits
- A page is one Firestore document (1 MB) — use sub-pages for large content.
- Simultaneous edits to the same page: last save wins.
