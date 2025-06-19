using Microsoft.Maui.Controls;
using Microsoft.Extensions.Logging;
using System;

namespace Game
{
    /// @class MainPage
    /// @brief The main page of the application
    /// @details This class handles the main user interface and navigation logic
    ///          for the primary page of the application
    public partial class MainPage : ContentPage
    {
        private readonly ILogger<MainPage> _logger;

        /// @brief Constructor for the MainPage class
        /// @details Initializes the components and sets up the user interface
        public MainPage(ILogger<MainPage> logger)
        {
            _logger = logger;
            _logger.LogInformation("Initializing MainPage...");
            InitializeComponent();
            _logger.LogInformation("MainPage initialized.");
        }

        /// @brief Event handler for the join session button click
        /// @param sender The object that triggered the event
        /// @param e The event arguments
        /// @details Opens a modal navigation page for joining a session
        private async void OnJoinSessionClicked(object sender, EventArgs e)
        {
            _logger.LogInformation("Join Session button clicked.");
            await Navigation.PushModalAsync(new NavigationPage(new JoinSessionPage()));
        }

        /// @brief Event handler for the exit button click
        /// @param sender The object that triggered the event
        /// @param e The event arguments
        /// @details Closes the main window of the application
        private void OnExitClicked(object sender, EventArgs e)
        {
            _logger.LogInformation("Exit button clicked – closing application.");
            System.Diagnostics.Process.GetCurrentProcess().CloseMainWindow();
        }
    }
}
