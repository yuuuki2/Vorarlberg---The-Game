using Microsoft.Extensions.Logging;

namespace Game;

/// @class CardDeckPage
/// @brief Page class for managing the card deck interface
/// @details Handles the display and interaction with the game's
///          card deck system
public partial class CardDeckPage : ContentPage
{
    private readonly ILogger<CardDeckPage> _logger;

    /// @brief Constructor for CardDeckPage
    /// @details Initializes the card deck page components
    public CardDeckPage(ILogger<CardDeckPage> logger)
    {
        _logger = logger;
        _logger.LogInformation("Initializing CardDeckPage...");

        InitializeComponent();

        _logger.LogInformation("CardDeckPage initialized.");
    }
}
