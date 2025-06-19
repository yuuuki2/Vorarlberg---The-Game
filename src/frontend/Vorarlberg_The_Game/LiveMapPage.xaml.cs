using Microsoft.Maui.Controls.Maps; // For Map, MapSpan
using Microsoft.Maui.Devices.Sensors; // For Geolocation, Location
using Microsoft.Maui.Maps; // For Distance (and other map-related types)
using System.Diagnostics;
using Microsoft.Maui.Controls;


// Resources/raw/leaflet-map.html
namespace Game
{
    /// @class LiveMapPage
    /// @brief Page class for displaying and managing the live map functionality
    /// @details This class handles the map display, location tracking, and
    ///          navigation controls for the live map feature
    public partial class LiveMapPage : ContentPage
    {
        /// @brief The main map control instance
        private readonly Microsoft.Maui.Controls.Maps.Map MyMap;

        /// @brief Flag for using alternative layout configuration
        private const bool UseAlternativeLayout = true;

        /// @brief Constructor for LiveMapPage
        /// @details Initializes the map components and sets up navigation buttons
        public LiveMapPage()
        {
            InitializeComponent();
            SetupButtonIcons();
            MyMap = new Microsoft.Maui.Controls.Maps.Map();
        }

        private Microsoft.Maui.Controls.Maps.Map GetMyMap()
        {
            return MyMap;
        }

        private void SetupButtonIcons()
        {
            if (UseAlternativeLayout)
            {
                // Konfiguration 2: question.png, curse.png
                Button0.Source = "question.png";
                Button1.Source = "curse.png";
            }
            else
            {
                // Konfiguration 1: carddeck.png, question.png
                Button0.Source = "carddeck.png";
                Button1.Source = "question.png";
            }
        }

        private async void OnButton0Clicked(object sender, EventArgs e)
        {
            if (UseAlternativeLayout)
                await Navigation.PushModalAsync(new NavigationPage(new QuestionsPage()));
            else
                await Navigation.PushModalAsync(new NavigationPage(new CardDeckPage()));
        }

        private async void OnButton1Clicked(object sender, EventArgs e)
        {
            if (UseAlternativeLayout)
                await Navigation.PushModalAsync(new NavigationPage(new CursesPage()));
            else
                await Navigation.PushModalAsync(new NavigationPage(new QuestionsPage()));
        }

        private async void OnButton2Clicked(object sender, EventArgs e)
        {
            await Navigation.PushModalAsync(new NavigationPage(new InfoPage()));
        }

        private async void OnButton3Clicked(object sender, EventArgs e)
        {
            await Navigation.PushModalAsync(new NavigationPage(new WuerfelPage(new WuerfelViewModel())));
        }


        private async void LoadLocation(Microsoft.Maui.Controls.Maps.Map MyMap)
        {
            try
            {
                // Fordert genaue Standortdaten an
                var request = new GeolocationRequest(GeolocationAccuracy.Medium, TimeSpan.FromSeconds(10));
                var location = await Geolocation.GetLocationAsync(request);

                if (location != null)
                {
                    // Zentriert die Karte auf den aktuellen Standort
                    MyMap.MoveToRegion(MapSpan.FromCenterAndRadius(
                        new Location(location.Latitude, location.Longitude),
                        Distance.FromKilometers(1))); // Zoom-Level 1km Radius
                }
                else
                {
                    Debug.WriteLine("Standort konnte nicht abgerufen werden.");
                    MyMap.MoveToRegion(MapSpan.FromCenterAndRadius(
                        new Location(47.2490, 9.9790), // Bregenz
                        Distance.FromKilometers(10)));
                }
            }
            catch (FeatureNotSupportedException fnsEx)
            {
                // Handle not supported on device exception
                Debug.WriteLine($"Feature not supported: {fnsEx.Message}");
                await DisplayAlert("Fehler", "Standortdienste werden auf diesem Ger�t nicht unterst�tzt.", "OK");
                MyMap.MoveToRegion(MapSpan.FromCenterAndRadius(
                    new Location(47.2490, 9.9790), // Bregenz
                    Distance.FromKilometers(10)));
            }
            catch (FeatureNotEnabledException fneEx)
            {
                // Handle not enabled on device exception
                Debug.WriteLine($"Feature not enabled: {fneEx.Message}");
                await DisplayAlert("Fehler", "Standortdienste sind nicht aktiviert. Bitte aktivieren Sie sie in den Ger�teeinstellungen.", "OK");
                MyMap.MoveToRegion(MapSpan.FromCenterAndRadius(
                    new Location(47.2490, 9.9790), // Bregenz
                    Distance.FromKilometers(10)));
            }
            catch (PermissionException pEx)
            {
                // Handle permission exception
                Debug.WriteLine($"Permission denied: {pEx.Message}");
                await DisplayAlert("Fehler", "Standortberechtigung verweigert. Bitte erteilen Sie die Berechtigung in den App-Einstellungen.", "OK");
                MyMap.MoveToRegion(MapSpan.FromCenterAndRadius(
                    new Location(47.2490, 9.9790), // Bregenz
                    Distance.FromKilometers(10)));
            }
            catch (Exception ex)
            {
                // Unable to get location
                Debug.WriteLine($"Unable to get location: {ex.Message}");
                await DisplayAlert("Fehler", $"Ein Fehler ist beim Abrufen des Standorts aufgetreten: {ex.Message}", "OK");
                // Fallback auf einen Standardstandort
                MyMap.MoveToRegion(MapSpan.FromCenterAndRadius(
                    new Location(47.2490, 9.9790), // Bregenz
                    Distance.FromKilometers(10)));
            }
        }

        private void OnWebViewNavigating(object sender, WebNavigatingEventArgs e)
        {
            if (!e.Url.StartsWith("file://", StringComparison.Ordinal))
            {
                e.Cancel = true;
            }
        }

        // �ndere R�ckgabetyp von void auf async Task
        private async Task LoadHtmlContent()
        {
            try
            {
                using var stream = await FileSystem.OpenAppPackageFileAsync("leaflet-map.html");
                using var reader = new StreamReader(stream);
                string html = await reader.ReadToEndAsync();
                MapWebView.Source = new HtmlWebViewSource { Html = html };
            }
            catch (Exception ex)
            {
                Debug.WriteLine($"Fehler beim Laden der HTML: {ex.Message}");
            }
        }

        protected override async void OnAppearing()
        {
            base.OnAppearing();
            await LoadHtmlContent();

            // Kurze Verz�gerung f�r Karteninitialisierung
            await Task.Delay(500);
            await GetCurrentLocation();
        }

        private async void OnWebViewNavigated(object sender, WebNavigatedEventArgs e)
        {
            if (e.Result == WebNavigationResult.Success)
            {
                await GetCurrentLocation();
            }
        }



        private async Task GetCurrentLocation()
        {
            try
            {
                var request = new GeolocationRequest(GeolocationAccuracy.Medium, TimeSpan.FromSeconds(10));
                var location = await Geolocation.GetLocationAsync(request);

                if (location != null)
                {
                    // JavaScript-Funktion im WebView aufrufen
                    await MapWebView.EvaluateJavaScriptAsync(
                        $"updatePosition({location.Latitude}, {location.Longitude})");
                }
            }
            catch (Exception ex)
            {
                Debug.WriteLine($"Fehler bei Standortabfrage: {ex.Message}");
                // Fallback zu Bregenz
                await MapWebView.EvaluateJavaScriptAsync(
                    $"updatePosition(47.2490, 9.9790)");
            }
        }

        private async void OnLocationClicked(object sender, EventArgs e)
        {
            await GetCurrentLocation();
        }

        private async void OnCenterClicked(object sender, EventArgs e)
        {
            await MapWebView.EvaluateJavaScriptAsync("centerVorarlberg()");
        }

        private async void OnMenuClicked(object sender, EventArgs e)
        {
            // Zur�ck zum Hauptmen� navigieren
            await Navigation.PopAsync();
        }
    }
}