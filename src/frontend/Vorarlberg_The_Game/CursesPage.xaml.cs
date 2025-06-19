using System.Collections.Generic;
using Microsoft.Maui.Controls;
using Microsoft.Extensions.Logging;

namespace Game
{
    /// @class CursesPage
    /// @brief Page for displaying active curses
    /// @details Shows all currently active curses affecting the Seekers,
    ///          including their effects and duration
    public partial class CursesPage : ContentPage
    {
        private readonly ILogger<CursesPage> _logger;

        /// @brief Constructor for CursesPage
        /// @details Initializes the page with hardcoded example curses
        public CursesPage(ILogger<CursesPage> logger)
        {
            _logger = logger;
            _logger.LogInformation("Initializing CursesPage...");

            InitializeComponent();

            // Example curses
            CursesView.ItemsSource = new List<string>
            {
                "Slow",
                "Blind",
                "Confusion"
            };

            _logger.LogInformation("CursesPage initialized with sample curses.");
        }

        /// <summary>
        /// Navigiert zurück zur LiveMapPage.
        /// </summary>
        private async void OnBackClicked(object sender, System.EventArgs e)
        {
            _logger.LogInformation("Back button clicked – navigating to LiveMapPage...");
            await Navigation.PopModalAsync();
        }
    }
}
