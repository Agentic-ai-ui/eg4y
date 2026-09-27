import { useState } from "react";
import { Alert, ScrollView, StyleSheet, Switch, Text, View } from "react-native";
import { router } from "expo-router";
import { DestructiveRow, LinkRow, ListSection } from "../../components/ListRow";
import { FloatingButton } from "../../components/FloatingButton";
import { useReduceMotion } from "../../components/useReduceMotion";
import { dynamicTypeRamp, minimumHitTarget, systemColor, textStyles } from "../../theme/tokens.native";

export default function LibraryScreen() {
  const [sync, setSync] = useState(true);
  const reduceMotion = useReduceMotion();

  // A native alert: specific title, verb buttons, "Cancel" to cancel, destructive style (CMP-12 – CMP-14).
  const confirmDeleteAll = () =>
    Alert.alert("Delete all books?", "This removes 128 books from this device.", [
      { text: "Cancel", style: "cancel" },
      { text: "Delete", style: "destructive", onPress: () => {} },
    ]);

  return (
    <View style={styles.screen}>
      {/* "automatic" lets the large title and tab bar inset the content (LAY-02) */}
      <ScrollView contentInsetAdjustmentBehavior="automatic" contentContainerStyle={styles.content}>
        <ListSection header="Collections">
          <LinkRow title="All Books" value="128" onPress={() => router.push("/library/all")} />
          <LinkRow title="Reading Now" value="3" onPress={() => router.push("/library/reading")} />
        </ListSection>
        <ListSection header="Options">
          <View style={styles.switchRow}>
            <Text style={[textStyles.body, styles.flex]} dynamicTypeRamp={dynamicTypeRamp.body}>
              iCloud Sync
            </Text>
            <Switch value={sync} onValueChange={setSync} accessibilityLabel="iCloud Sync" />
          </View>
        </ListSection>
        <ListSection>
          <DestructiveRow title="Delete All" onPress={confirmDeleteAll} />
        </ListSection>
        {reduceMotion ? null : <Text style={styles.hint}>Tip: pull down to refresh.</Text>}
      </ScrollView>
      <View style={styles.floating}>
        <FloatingButton label="Add Book" symbol="plus" onPress={() => router.push("/library/new")} />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: systemColor("groupedBackground") },
  content: { padding: 16 },
  switchRow: { minHeight: minimumHitTarget, flexDirection: "row", alignItems: "center", paddingHorizontal: 16, paddingVertical: 8 },
  flex: { flex: 1, color: systemColor("label") },
  hint: { ...textStyles.footnote, color: systemColor("secondaryLabel"), paddingHorizontal: 16 },
  floating: { position: "absolute", right: 16, bottom: 16 },
});
