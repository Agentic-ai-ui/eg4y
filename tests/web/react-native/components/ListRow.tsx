import { Pressable, StyleSheet, Text, View } from "react-native";
import { SymbolView } from "expo-symbols";
import { dynamicTypeRamp, minimumHitTarget, systemColor, textStyles } from "../theme/tokens.native";

/** A navigation row: 44 pt minimum height, system colors, Dynamic Type, a VoiceOver-friendly role. */
export function LinkRow({ title, value, onPress }: { title: string; value?: string; onPress: () => void }) {
  return (
    <Pressable
      role="link"
      accessibilityLabel={value ? `${title}, ${value}` : title}
      onPress={onPress}
      style={({ pressed }) => [styles.row, pressed && { backgroundColor: systemColor("systemGray5") }]}
    >
      <Text style={[textStyles.body, styles.title]} dynamicTypeRamp={dynamicTypeRamp.body}>{title}</Text>
      {value ? (
        <Text style={[textStyles.body, { color: systemColor("secondaryLabel") }]} dynamicTypeRamp={dynamicTypeRamp.body}>
          {value}
        </Text>
      ) : null}
      <SymbolView
        name={{ ios: "chevron.forward", android: "chevron_right", web: "chevron_right" }}
        size={14}
        tintColor={systemColor("systemGray3")}
      />
    </Pressable>
  );
}

/** A destructive action row, such as “Delete All” (CMP-14). */
export function DestructiveRow({ title, onPress }: { title: string; onPress: () => void }) {
  return (
    <Pressable role="button" onPress={onPress} style={styles.row}>
      <Text style={[textStyles.body, { color: systemColor("red") }]} dynamicTypeRamp={dynamicTypeRamp.body}>{title}</Text>
    </Pressable>
  );
}

export function ListSection({ header, children }: { header?: string; children: React.ReactNode }) {
  return (
    <View style={styles.section}>
      {header ? (
        <Text role="heading" style={[textStyles.footnote, styles.header]} dynamicTypeRamp={dynamicTypeRamp.footnote}>
          {header}
        </Text>
      ) : null}
      <View style={styles.group}>{children}</View>
    </View>
  );
}

const styles = StyleSheet.create({
  section: { marginBottom: 24 },
  header: { paddingHorizontal: 16, paddingBottom: 6, fontWeight: "600", color: systemColor("secondaryLabel") },
  group: { borderRadius: 12, overflow: "hidden", backgroundColor: systemColor("secondaryBackground") },
  row: {
    minHeight: minimumHitTarget,
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
    paddingHorizontal: 16,
    paddingVertical: 10,
  },
  title: { flex: 1, color: systemColor("label") },
});
