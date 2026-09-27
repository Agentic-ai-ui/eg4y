import { DynamicColorIOS, Platform, type ColorValue } from "react-native";

// A brand color with all four variants, like an asset-catalog Color Set (COL-02).
// Check every variant for 4.5:1 against the backgrounds it sits on (COL-06).
export const brandTint: ColorValue =
  Platform.OS === "ios"
    ? DynamicColorIOS({
        light: "#8A3FFC",
        dark: "#A56EFF",
        highContrastLight: "#6929C4",
        highContrastDark: "#BE95FF",
      })
    : "#8A3FFC";
