/// @file App.xaml.cs
/// @brief Main application class that serves as the entry point for the MAUI application
/// @details This class initializes the application and sets up the main navigation shell

namespace Game
{
    /// @class App
    /// @brief The main application class that inherits from MAUI Application
    /// @details Handles the initialization of the application and sets up the initial navigation
    public partial class App : Application
    {
        /// @brief Constructor for the App class
        /// @details Initializes the application and sets the main page to AppShell
        public App()
        {
            MainPage = new AppShell();
        }
    }
}
