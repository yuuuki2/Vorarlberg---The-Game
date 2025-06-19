using Microsoft.Maui.Controls.Maps;
using Microsoft.Maui.Devices.Sensors;
using Microsoft.Maui.Maps;
using Microsoft.Maui.Controls;
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using Microsoft.Maui.Platform;

namespace Game
{
    /// @class LiveMapPage
    /// @brief Page class for displaying and managing the live map functionality
    /// @details This class handles the map display, location tracking, and
    ///          navigation controls for the live map feature
    public partial class LiveMapPage : ContentPage
    {
        private readonly Microsoft.Maui.Controls.Maps.Map MyMap;
        private readonly ILogger<LiveMapPage> _logger;

        private const bool UseAlternativeLayout = true;

        public LiveMapPage(ILogger<LiveMapPage> logger)
        {
            _logger = logger;
            _logger.LogInformation("Initializing LiveMapPage...");

            InitializeComponent();
            SetupButtonIcons();
            MyMap = new Microsoft.Maui.Controls.Maps.Map();

            _logger.LogInformation("LiveMapPage initialized.");
        }

        private Microsoft.Maui.Controls.Maps.Map GetMyMap() => MyMap;

        private void SetupButtonIcons()
        {
            _logger.LogInformation("Setting up button icons (Layout: {Layout})", UseAlternativeLayout ? "Alternative" : "Default");

            if (UseAlternativeLayout)
            {
                Button0.Source = "question.png";
                Button1.Source = "curse.png";
            }
            else
            {
                Button0.Source = "carddeck.png";
                Button1.Source = "question.png";
            }
        }

        private async void OnButton0Clicked(object sender, EventArgs e)
        {
            _logger.LogInformation("Button0 clicked.");
            if (UseAlternativeLayout)
                await Navigation.PushModalAsync(new NavigationPage(new QuestionsPage()));
            else
                await Navigation.PushModalAsync(new NavigationPage(new CardDeckPage()));
        }

        private async void OnButton1Clicked(object sender, EventArgs e)
        {
            _logger.LogInformation("Button1 clicked.");
            if (UseAlternativeLayout)
                await Navigation.PushModalAsync(new NavigationPage(new CursesPage()));
            else
                await Navigation.PushModalAsync(new NavigationPage(new QuestionsPage()));
        }

        private async void OnButton2Clicked(object sender, EventArgs e)
        {
            _logger.LogInformation("Button2 (Info) clicked.");
            await Navigation.PushModalAsync(new NavigationPage(new InfoPage()));
        }

        private async void OnButton3Clicked(object sender, EventArgs e)
        {
            _logger.LogInformation("Button3 (Wuerfel) clicked.");
            await Navigation.PushModalAsync(new NavigationPage(new WuerfelPage(new WuerfelViewModel())));
        }

        private async void LoadLocation(Microsoft.Maui.Controls.Maps.Map MyMap)
        {
            try
            {
                _logger.LogInformation("Loading user location...");
                var request = new GeolocationRequest(GeolocationAccuracy.Medium, TimeSpan.FromSeconds(10));
                var location = await Geolocation.GetLocationAsync(request);

                if (location != null)
                {
                    _logger.LogInformation("Location acquired: {Lat}, {Lng}", location.Latitude, location.Longitude);
                    MyMap.MoveToRegion(MapSpan.FromCenterAndRadius(
                        new Location(location.Latitude, location.Longitude),
                        Distance.FromKilometers(1)));
                }
                else
                {
                    _logger.LogWarning("Location is null. Falling back to default.");
                    MyMap.MoveToRegion(MapSpan.FromCenterAndRadius(
                        new Location(47.2490, 9.9790),
                        Distance.FromKilometers(10)));
                }
            }
            catch (FeatureNotSupportedException ex)
            {
                _logger.LogError(ex, "Location not supported.");
                await DisplayAlert("Fehler", "Standortdienste werden auf diesem Gerät nicht unterstützt.", "OK");
            }
            catch (FeatureNotEnabledException ex)
            {
                _logger.LogError(ex, "Location not enabled.");
                await DisplayAlert("Fehler", "Standortdienste sind nicht aktiviert.", "OK");
            }
            catch (PermissionException ex)
            {
                _logger.LogError(ex, "Location permission denied.");
                await DisplayAlert("Fehler", "Standortberechtigung verweigert.", "OK");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Unexpected error while getting location.");
                await DisplayAlert("Fehler", $"Ein Fehler ist beim Abrufen des Standorts aufgetreten: {ex.Message}", "OK");
            }

            // Always fallback
            MyMap.MoveToRegion(MapSpan.FromCenterAndRadius(new Location(47.2490, 9.9790), Distance.FromKilometers(10)));
        }

        private void OnWebViewNavigating(object sender, WebNavigatingEventArgs e)
        {
            if (!e.Url.StartsWith("file://", StringComparison.Ordinal))
            {
                _logger.LogWarning("Blocked navigation to non-local URL: {Url}", e.Url);
                e.Cancel = true;
            }
        }

        private async Task LoadHtmlContent()
        {
            try
            {
                _logger.LogInformation("Loading leaflet HTML...");
                using var stream = await FileSystem.OpenAppPackageFileAsync("leaflet-map.html");
                using var reader = new StreamReader(stream);
                string html = await reader.ReadToEndAsync();
                MapWebView.Source = new HtmlWebViewSource { Html = html };
                _logger.LogInformation("HTML content loaded into WebView.");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to load HTML content.");
            }
        }

        protected override async void OnAppearing()
        {
            base.OnAppearing();
            _logger.LogInformation("LiveMapPage appeared.");
            await LoadHtmlContent();
            await Task.Delay(500);
            await GetCurrentLocation();
        }

        private async void OnWebViewNavigated(object sender, WebNavigatedEventArgs e)
        {
            if (e.Result == WebNavigationResult.Success)
            {
                _logger.LogInformation("WebView finished navigating – calling GetCurrentLocation.");
                await GetCurrentLocation();
            }
            else
            {
                _logger.LogWarning("WebView navigation failed: {Result}", e.Result);
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
                    _logger.LogInformation("Updating map with current location: {Lat}, {Lng}", location.Latitude, location.Longitude);
                    await MapWebView.EvaluateJavaScriptAsync($"updatePosition({location.Latitude}, {location.Longitude})");
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error during location update.");
                await MapWebView.EvaluateJavaScriptAsync($"updatePosition(47.2490, 9.9790)");
            }
        }

        private async void OnLocationClicked(object sender, EventArgs e)
        {
            _logger.LogInformation("Location button clicked.");
            await GetCurrentLocation();
        }

        private async void OnCenterClicked(object sender, EventArgs e)
        {
            _logger.LogInformation("Center Vorarlberg button clicked.");
            await MapWebView.EvaluateJavaScriptAsync("centerVorarlberg()");
        }

        private async void OnMenuClicked(object sender, EventArgs e)
        {
            _logger.LogInformation("Back to main menu clicked.");
            await Navigation.PopAsync();
        }
    }
}
