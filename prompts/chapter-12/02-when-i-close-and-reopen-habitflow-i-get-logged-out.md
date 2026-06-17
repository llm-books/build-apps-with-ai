# When I close and reopen HabitFlow, I get logged out and…

**Chapter 12 — User Accounts And Cloud Sync**  
Used in: Step 5

---

```
When I close and reopen HabitFlow, I get logged out and have to sign in again. The login should persist between app restarts. Make sure firebase.ts uses initializeAuth with getReactNativePersistence and AsyncStorage instead of getAuth(). The getAuth() function does not persist auth state in React Native.
```
