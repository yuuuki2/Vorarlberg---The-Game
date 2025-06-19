using CommunityToolkit.Maui;
using Microsoft.Extensions.Logging;
using SkiaSharp.Views.Maui.Controls.Hosting;

namespace Game
{
    /// @class MauiProgram
    /// @brief Static class that configures and creates the MAUI application
    /// @details This class is responsible for setting up the application's dependencies,
    ///          including fonts, services, and third-party libraries
    public static class MauiProgram
    {
        /// @brief Creates and configures the MAUI application
        /// @return A configured MauiApp instance
        /// @details Sets up the application builder with required services,
        ///          including MAUI maps, community toolkit, SkiaSharp, and custom fonts
        public static MauiApp CreateMauiApp()
        {
            var builder = MauiApp.CreateBuilder();
            builder
                .UseMauiApp<App>()
                .UseMauiMaps()
                .UseMauiCommunityToolkit()
                .UseSkiaSharp()
                .ConfigureFonts(fonts =>
                {
                    fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
                    fonts.AddFont("OpenSans-Semibold.ttf", "OpenSansSemibold");
                    fonts.AddFont("fa-solid-900.ttf", "FontAwesome");
                });

            builder.Logging.AddDebug();


            return builder.Build();
        }
    }
}