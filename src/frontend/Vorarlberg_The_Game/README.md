````markdown
# MAUI-Demo: WürfelPage & BushalteSuchen

---

## 1. Übersicht

Dieses kleine MAUI-Projekt enthält zwei einfache Seiten:

1. **WürfelPage**  
   - Simuliert das Werfen eines sechsseitigen Würfels.  
2. **BushalteSuchen**  
   - Eine Demonstrationsseite zur (fiktiven) Suche nach Bushaltestellen.

Beide Komponenten sind bewusst minimal gehalten, um die Grundlagen von MVVM und SkiaSharp in MAUI kennenzulernen.

---

## 2. Voraussetzungen

- [.NET 8 SDK](https://dotnet.microsoft.com/)  
- MAUI-Workload installiert (`dotnet workload install maui`)

---

## 3. Abhängigkeiten

Führe im Projektordner folgende Befehle aus, um die benötigten NuGet-Pakete hinzuzufügen:

```bash
dotnet add package CommunityToolkit.Mvvm --version 8.4.0
dotnet add package CommunityToolkit.Maui --version 8.0.1
dotnet add package SkiaSharp.Views.Maui.Controls --version 3.119.0

````

### Windows-spezifisch

Um Versionskonflikte mit dem Windows SDK zu vermeiden, ergänze in Deiner `.csproj`:

```xml
<PropertyGroup>
  <WindowsSdkPackageVersion>10.0.19041.53</WindowsSdkPackageVersion>
</PropertyGroup>
```

---

## 4. Projektaufbau

1. **Restore**

   ```bash
   dotnet restore
   ```
2. **Build**

   ```bash
   dotnet build -p:WindowsSdkPackageVersion=10.0.19041.53
   ```

   Unter Windows genügt in der Regel auch:

   ```bash
   dotnet build
   ```

Nach erfolgreichem Build liegen die Assemblies im Ordner `bin/Debug`.

---

## 5. Ordnerstruktur

```
/Game
  ├── App.xaml
  │     └── App.xaml.cs
  MainPage.xaml
  │     └── MainPage.xaml.cs
  ├── Styles.xaml
  ├── WürfelPage.xaml
  │     └── WuerfelPage.xaml.cs
  ├── BushalteSuchenPage.xaml
  │     └── BushalteSuchenPage.xamll.cs
  ├── ViewModels
  │     ├── WürfelViewModel.cs
  │     └── BushalteViewModel.cs
  └── Resources
        └── Images
             ├── dice1.png
             ├── dice2.png
             ├── dice3.png
             ├── dice4.png
             ├── dice5.png
             └── dice6.png
```

---

## 6. Icons und Lizenz

Die Würfel-Grafiken stammen von **game-icons.net** und stehen unter der Lizenz **CC BY 3.0**. Bitte achte auf die Namensnennung, wenn Du die Bilder wiederverwendest.

* **Quelle:**
  [https://game-icons.net/tags/dice.html](https://game-icons.net/tags/dice.html)
* **Lizenz:**
  Creative Commons Attribution 3.0 Unported (CC BY 3.0)
  – Erlaubt: Teilen und Bearbeiten, auch kommerziell
  – Bedingung: Namensnennung des Urhebers

**Im Projekt enthaltene Dateien:**

```
Resources/Images/dice1.png  
Resources/Images/dice2.png  
Resources/Images/dice3.png  
Resources/Images/dice4.png  
Resources/Images/dice5.png  
Resources/Images/dice6.png  
```