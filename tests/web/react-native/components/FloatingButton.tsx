import { Pressable, StyleSheet, View } from "react-native";
import { GlassView, isGlassEffectAPIAvailable } from "expo-glass-effect";
import { SymbolView, type SFSymbol } from "expo-symbols";
import { minimumHitTarget, systemColor } from "../theme/tokens.native";

/**
 * A floating control in the Liquid Glass layer (iOS 26+), with a plain fallback elsewhere.
 * Glass belongs to controls and navigation only — never to content (GLS-01) — and never stacks on glass (GLS-03).
 */
export function FloatingButton({ label, symbol, onPress }: { label: string; symbol: SFSymbol; onPress: () => void }) {
  const Surface = isGlassEffectAPIAvailable() ? GlassView : View;
  return (
    <Surface style={[styles.surface, !isGlassEffectAPIAvailable() && { backgroundColor: systemColor("secondaryBackground") }]}>
      <Pressable role="button" accessibilityLabel={label} onPress={onPress} hitSlop={8} style={styles.button}>
        <SymbolView name={{ ios: symbol, android: "add", web: "add" }} size={22} tintColor={systemColor("blue")} />
      </Pressable>
    </Surface>
  );
}

const styles = StyleSheet.create({
  surface: { borderRadius: 999, overflow: "hidden" },
  button: { minWidth: minimumHitTarget + 8, minHeight: minimumHitTarget + 8, alignItems: "center", justifyContent: "center" },
});
