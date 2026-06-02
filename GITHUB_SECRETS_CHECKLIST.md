# GitHub Actions secrets checklist

Add these in **GitHub → Settings → Secrets and variables → Actions** (repository or environment).
Values are never committed here — only names and hints.

| Secret | Optional | Used in workflows | Where to get it |
| --- | --- | --- | --- |
| `APP_STORE_CONNECT_API_KEY` | no | rn-job-ios-build-bare.yml, rn-job-ios-internal-release-bare.yml | App Store Connect API key — private key (.p8) contents. |
| `APP_STORE_CONNECT_ISSUER_ID` | no | rn-job-ios-build-bare.yml, rn-job-ios-internal-release-bare.yml | App Store Connect API key — Issuer ID. |
| `APP_STORE_CONNECT_KEY_ID` | no | rn-job-ios-build-bare.yml, rn-job-ios-internal-release-bare.yml | App Store Connect API key — Key ID. |
| `DIST_CERTIFICATE_BASE64` | no | rn-job-ios-build-bare.yml, rn-job-ios-firebase-release-bare.yml, rn-job-ios-internal-release-bare.yml | Distribution signing certificate (.p12) base64. |
| `DIST_CERTIFICATE_DEV_BASE64` | yes | rn-job-ios-firebase-release-bare.yml | Development / ad-hoc certificate base64 (iOS Firebase dev builds). |
| `DIST_CERTIFICATE_DEV_PASSWORD` | yes | rn-job-ios-firebase-release-bare.yml | Password for dev signing .p12. |
| `DIST_CERTIFICATE_PASSWORD` | no | rn-job-ios-build-bare.yml, rn-job-ios-firebase-release-bare.yml, rn-job-ios-internal-release-bare.yml | Password for the distribution .p12. |
| `DIST_PROFILE_BASE64` | no | rn-job-ios-build-bare.yml, rn-job-ios-firebase-release-bare.yml, rn-job-ios-internal-release-bare.yml | Provisioning profile (.mobileprovision) base64 for distribution. |
| `DIST_PROFILE_DEV_BASE64` | yes | rn-job-ios-firebase-release-bare.yml | Development provisioning profile base64. |
| `EXPO_TOKEN` | yes | rn-job-android-build-expo.yml, rn-job-android-internal-release-expo.yml, rn-job-expo-eas-build-and-distribute.yml, rn-job-ios-build-expo-cloud.yml, rn-job-ios-build-expo-local.yml, rn-job-ios-internal-release-expo.yml | Expo account → https://expo.dev/accounts/[account]/settings/access-tokens (EAS / Expo workflows). |
| `FIREBASE_ANDROID_APP_ID` | yes | rn-job-android-firebase-release-bare.yml, rn-job-expo-eas-build-and-distribute.yml | Firebase Console → Project settings → Your apps → Android (prod / dist applicationId). |
| `FIREBASE_ANDROID_DEV_APP_ID` | yes | rn-job-android-firebase-release-bare.yml, rn-job-expo-eas-build-and-distribute.yml | Firebase Android app for the dev applicationId. |
| `FIREBASE_IOS_APP_ID` | yes | rn-job-expo-eas-build-and-distribute.yml, rn-job-ios-firebase-release-bare.yml | Firebase iOS app ID for distribution / prod bundle. |
| `FIREBASE_IOS_DEV_APP_ID` | yes | rn-job-expo-eas-build-and-distribute.yml, rn-job-ios-firebase-release-bare.yml | Firebase iOS app ID for dev bundle. |
| `FIREBASE_SERVICE_ACCOUNT_JSON` | yes | rn-job-android-firebase-release-bare.yml, rn-job-expo-eas-build-and-distribute.yml, rn-job-ios-firebase-release-bare.yml | Firebase service account JSON with App Distribution Admin (or broader) for CI. |
| `GOOGLE_SERVICES_JSON` | yes | rn-job-android-build-bare.yml, rn-job-android-build-expo.yml, rn-job-android-debug-apk.yml, rn-job-android-firebase-release-bare.yml, rn-job-android-internal-release-bare.yml, rn-job-android-perf.yml, rn-job-expo-eas-build-and-distribute.yml, rn-job-ios-build-bare.yml, rn-job-ios-build-expo-cloud.yml, rn-job-ios-build-expo-local.yml, rn-job-ios-firebase-release-bare.yml, rn-job-ios-internal-release-bare.yml, rn-job-ios-performance.yml, rn-job-ios-simulator-artifact.yml, rn-job-ios-test.yml, rn-performance-baseline.yml | Full google-services.json from Firebase Console (Android; may include all flavor package_name clients). |
| `GOOGLE_SERVICE_INFO_PLIST` | yes | rn-job-android-build-bare.yml, rn-job-android-build-expo.yml, rn-job-android-debug-apk.yml, rn-job-android-firebase-release-bare.yml, rn-job-android-internal-release-bare.yml, rn-job-android-perf.yml, rn-job-expo-eas-build-and-distribute.yml, rn-job-ios-build-bare.yml, rn-job-ios-build-expo-cloud.yml, rn-job-ios-build-expo-local.yml, rn-job-ios-firebase-release-bare.yml, rn-job-ios-internal-release-bare.yml, rn-job-ios-performance.yml, rn-job-ios-simulator-artifact.yml, rn-job-ios-test.yml, rn-performance-baseline.yml | Optional fallback iOS plist when only one Firebase iOS app is used in CI. |
| `GOOGLE_SERVICE_INFO_PLIST_DEV` | yes | rn-job-android-build-bare.yml, rn-job-android-build-expo.yml, rn-job-android-debug-apk.yml, rn-job-android-firebase-release-bare.yml, rn-job-android-internal-release-bare.yml, rn-job-android-perf.yml, rn-job-expo-eas-build-and-distribute.yml, rn-job-ios-build-bare.yml, rn-job-ios-build-expo-cloud.yml, rn-job-ios-build-expo-local.yml, rn-job-ios-firebase-release-bare.yml, rn-job-ios-internal-release-bare.yml, rn-job-ios-performance.yml, rn-job-ios-simulator-artifact.yml, rn-job-ios-test.yml, rn-performance-baseline.yml | GoogleService-Info.plist for dev/QA bundle ID — restored in CI before iOS dev builds. |
| `GOOGLE_SERVICE_INFO_PLIST_DIST` | yes | rn-job-android-build-bare.yml, rn-job-android-build-expo.yml, rn-job-android-debug-apk.yml, rn-job-android-firebase-release-bare.yml, rn-job-android-internal-release-bare.yml, rn-job-android-perf.yml, rn-job-expo-eas-build-and-distribute.yml, rn-job-ios-build-bare.yml, rn-job-ios-build-expo-cloud.yml, rn-job-ios-build-expo-local.yml, rn-job-ios-firebase-release-bare.yml, rn-job-ios-internal-release-bare.yml, rn-job-ios-performance.yml, rn-job-ios-simulator-artifact.yml, rn-job-ios-test.yml, rn-performance-baseline.yml | GoogleService-Info.plist for production bundle ID — restored in CI before iOS dist/TestFlight builds. |
| `IOS_CODESIGN_IDENTITY` | yes | rn-job-ios-build-bare.yml, rn-job-ios-firebase-release-bare.yml, rn-job-ios-internal-release-bare.yml | Codesign identity string shown by `security find-identity -v -p codesigning` on the runner keychain setup. |
| `PERF_ANDROID_RUNNER` | no | rn.yml | See the referenced workflow job and your store / Firebase / Play consoles. |
| `PERF_IOS_RUNNER` | no | rn.yml | See the referenced workflow job and your store / Firebase / Play consoles. |
| `PLAY_SERVICE_ACCOUNT_JSON` | no | rn-job-android-internal-release-bare.yml | Google Play service account JSON (Android internal release → Play Internal App Sharing). |
| `RELEASE_KEYSTORE_BASE64` | no | rn-job-android-firebase-release-bare.yml, rn-job-android-internal-release-bare.yml | Base64-encoded Android release keystore file. |
| `RELEASE_KEYSTORE_PASSWORD` | no | rn-job-android-firebase-release-bare.yml, rn-job-android-internal-release-bare.yml | Android keystore store password. |
| `RELEASE_KEY_ALIAS` | no | rn-job-android-firebase-release-bare.yml, rn-job-android-internal-release-bare.yml | Android keystore key alias. |
| `RELEASE_KEY_PASSWORD` | no | rn-job-android-firebase-release-bare.yml, rn-job-android-internal-release-bare.yml | Android keystore key password. |
| `SLACK_TRIGGER_WEBHOOK_URL` | yes | rn-job-android-firebase-release-bare.yml, rn-job-android-internal-release-bare.yml, rn-job-ios-firebase-release-bare.yml | Optional Slack Workflow Builder webhook trigger URL; workflow Text variable must be named message (see notify_slack_workflow_webhook.sh). |
| `SNYK_TOKEN` | yes | rn-job-security.yml | Optional — https://snyk.io ; if unset, Snyk step is skipped. |

_Generated by `.github/scripts/list_workflow_secrets.py` — re-run after you add or change workflows._
