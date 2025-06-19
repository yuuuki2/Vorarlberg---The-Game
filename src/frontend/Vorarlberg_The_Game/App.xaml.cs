/// @file App.xaml.cs
/// @brief Main application class that serves as the entry point for the MAUI application
/// @details This class initializes the application and sets up the main navigation shell

using Microsoft.Extensions.Logging;

namespace Game
{
    /// @class App
    /// @brief The main application class that inherits from MAUI Application
    /// @details Handles the initialization of the application and sets up the initial navigation
    public partial class App : Application
    {
        private readonly ILogger<App> _logger;

        /// @brief Constructor for the App class
        /// @details Initializes the application and sets the main page to AppShell
        public App(ILogger<App> logger, AppShell appShell)
        {
            _logger = logger;

            _logger.LogInformation("Initializing App...");
            MainPage = appShell;
            _logger.LogInformation("MainPage set to AppShell.");
        }
    }
}
