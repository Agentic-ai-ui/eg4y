import { Stack } from "expo-router";

// Native navigation stack with a large title that collapses on scroll (NAV-15).
// Leave the header background alone so the system renders its glass and scroll edge effect (GLS-04).
export default function LibraryLayout() {
  return (
    <Stack>
      <Stack.Screen name="index" options={{ title: "Library", headerLargeTitleEnabled: true }} />
    </Stack>
  );
}
