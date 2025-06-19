using Microsoft.Extensions.Logging;

namespace Game
{
    /// @class AppShell
    /// @brief The main shell class that provides navigation framework for the application
    /// @details This class inherits from Shell and provides the navigation structure
    ///          and routing capabilities for the application
    public partial class AppShell : Shell
    {
        private readonly ILogger<AppShell> _logger;

        /// @brief Constructor for the AppShell class
        /// @details Initializes the shell components and sets up navigation
        public AppShell(ILogger<AppShell> logger)
        {
            _logger = logger;
            _logger.LogInformation("Initializing AppShell...");

            InitializeComponent();

            _logger.LogInformation("AppShell initialized successfully.");
        }
    }
}
