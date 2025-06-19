using Microsoft.Maui.Controls;
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;

namespace Game;

/// @class JoinSessionPage
/// @brief Page class for handling session joining functionality
/// @details This class manages the user interface and logic for joining
///          an existing game session
public partial class JoinSessionPage : ContentPage
{
    private readonly ILogger<JoinSessionPage> _logger;

    /// @brief Constructor for the JoinSessionPage
    /// @details Initializes the components of the join session page
    public JoinSessionPage(ILogger<JoinSessionPage> logger)
    {
        _logger = logger;
        _logger.LogInformation("Initializing JoinSessionPage...");

        InitializeComponent();

        _logger.LogInformation("JoinSessionPage initialized.");
    }

    /// @brief Event handler for the join button click
    /// @param sender The object that triggered the event
    /// @param e The event arguments
    /// @details Validates the session code and attempts to join the session
    private async void OnJoinClicked(object sender, EventArgs e)
    {
        string sessionCode = SessionCodeEntry.Text;
        _logger.LogInformation("Join button clicked with session code: {SessionCode}", sessionCode);

        if (string.IsNullOrWhiteSpace(sessionCode))
        {
            _logger.LogWarning("Join attempt failed – session code was empty or whitespace.");
            await DisplayAlert("Error", "Please enter a session code.", "OK");
            return;
        }

        _logger.LogInformation("Session code valid. Joining session...");

        var players = new List<string> { "You", "Player 1", "Player 2" };

        await Navigation.PushModalAsync(new NavigationPage(new RoomPage(players)));
        _logger.LogInformation("Navigated to RoomPage with players: {Players}", string.Join(", ", players));
    }

    private async void OnBackClicked(object sender, EventArgs e)
    {
        _logger.LogInformation("Back button clicked – navigating back.");
        await Navigation.PopModalAsync();
    }
}
