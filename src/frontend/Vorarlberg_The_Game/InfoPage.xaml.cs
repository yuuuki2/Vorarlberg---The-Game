using Microsoft.Maui.Controls;

namespace Game
{
    /// @class InfoPage
    /// @brief Page class for displaying game information
    /// @details Manages and displays detailed information about the current
    ///          game session, including player roles and scores
    public partial class InfoPage : ContentPage
    {
        /// @brief Constructor for InfoPage
        /// @details Initializes the page with example game information
        ///          including role, start time, and current score
        public InfoPage()
        {
            InitializeComponent();

            // Beispiel-Game-Info
            RoleLabel.Text = "Hider";
            StartTimeLabel.Text = "2025-06-16 14:00";
            ScoreLabel.Text = "Hiders: 3 - Seekers: 2";
            ServerLabel.Text = "192.168.0.1:5000";

            // Beispiel-Player-Info
            YourCoordsLabel.Text = "47.2490, 9.9790";
            SeekerCoordsLabel.Text = "47.2500, 9.9800";
            YourMunicipalityLabel.Text = "Bregenz";
            SeekerMunicipalityLabel.Text = "Dornbirn";
            YourStationLabel.Text = "Hafenstra�e";
            SeekerStationLabel.Text = "Marktstra�e";
        }

        /// <summary>
        /// Navigiert zur�ck zur LiveMapPage.
        /// </summary>
        private async void OnBackClicked(object sender, System.EventArgs e)
        {
            await Navigation.PopModalAsync();
        }
    }
}
