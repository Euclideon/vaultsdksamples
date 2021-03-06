#ifndef VaultSDKFeatureSamples_h__
#define VaultSDKFeatureSamples_h__

// Euclideon does NOT recommend storing user credentials in this format
// This is only done to simplify the feature demonstrations

constexpr char s_VaultServer[] = "https://earth.vault.euclideon.com";
constexpr char s_VaultUsername[] = "";
constexpr char s_VaultPassword[] = "";

// Some helper macro's so that the sample code can remain fairly tidy
#define ExitWithMessage(resultCode, pMsg) do { printf("[" __FILE__ ":%d] %s", __LINE__, pMsg); exit(resultCode); } while(false)

#endif //VaultSDKFeatureSamples_h__
