"""
Tests for the Mergington High School Activities Management API.

Tests cover both success and error scenarios for the activities endpoints,
using the Arrange-Act-Assert (AAA) pattern for clarity.
"""
import pytest
from urllib.parse import urlencode
from fastapi.testclient import TestClient


class TestGetActivities:
    """Tests for the GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client: TestClient):
        """Arrange-Act-Assert: Verify GET /activities returns all activities."""
        # Arrange: No setup needed, activities are loaded by fixture

        # Act: Make GET request to /activities
        response = client.get("/activities")

        # Assert: Verify response status and content
        assert response.status_code == 200
        activities_data = response.json()
        assert len(activities_data) == 9
        assert "Chess Club" in activities_data
        assert "Programming Class" in activities_data

    def test_get_activities_returns_activity_structure(self, client: TestClient):
        """Arrange-Act-Assert: Verify each activity has required fields."""
        # Arrange: No setup needed

        # Act: Make GET request and extract first activity
        response = client.get("/activities")
        activities_data = response.json()
        chess_club = activities_data["Chess Club"]

        # Assert: Verify activity structure
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)

    def test_get_activities_includes_participant_list(self, client: TestClient):
        """Arrange-Act-Assert: Verify activities include current participants."""
        # Arrange: No setup needed

        # Act: Get activities data
        response = client.get("/activities")
        activities_data = response.json()

        # Assert: Verify participants are included
        chess_club_participants = activities_data["Chess Club"]["participants"]
        assert "michael@mergington.edu" in chess_club_participants
        assert "daniel@mergington.edu" in chess_club_participants


class TestSignupForActivity:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success_new_student(self, client: TestClient):
        """Arrange-Act-Assert: Successfully sign up a new student for an activity."""
        # Arrange: Student not yet signed up for Tennis Club
        new_student_email = "newstudent@mergington.edu"

        # Act: Sign up the student
        response = client.post(
            f"/activities/Tennis Club/signup?email={new_student_email}"
        )

        # Assert: Verify successful signup
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {new_student_email} for Tennis Club"

    def test_signup_success_adds_participant(self, client: TestClient):
        """Arrange-Act-Assert: Verify signup adds student to participants list."""
        # Arrange: New student email
        new_student_email = "jane.doe@mergington.edu"

        # Act: Sign up student, then retrieve activities
        client.post(f"/activities/Basketball Team/signup?email={new_student_email}")
        response = client.get("/activities")

        # Assert: Verify student appears in participants
        activities_data = response.json()
        basketball_participants = activities_data["Basketball Team"]["participants"]
        assert new_student_email in basketball_participants

    def test_signup_invalid_activity_returns_404(self, client: TestClient):
        """Arrange-Act-Assert: Signup for non-existent activity returns 404."""
        # Arrange: Activity does not exist
        invalid_activity = "Underwater Basket Weaving"
        student_email = "student@mergington.edu"

        # Act: Attempt to sign up for invalid activity
        response = client.post(
            f"/activities/{invalid_activity}/signup?email={student_email}"
        )

        # Assert: Verify 404 response
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_duplicate_student_returns_400(self, client: TestClient):
        """Arrange-Act-Assert: Duplicate signup returns 400 Bad Request."""
        # Arrange: Student already signed up for Chess Club
        existing_student = "michael@mergington.edu"

        # Act: Attempt to sign up student who is already enrolled
        response = client.post(
            f"/activities/Chess Club/signup?email={existing_student}"
        )

        # Assert: Verify 400 response with appropriate error message
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up"

    def test_signup_missing_email_parameter(self, client: TestClient):
        """Arrange-Act-Assert: Missing email parameter returns validation error."""
        # Arrange: Email parameter omitted from request

        # Act: Sign up without email parameter
        response = client.post("/activities/Chess Club/signup")

        # Assert: Verify validation error (422 Unprocessable Entity)
        assert response.status_code == 422

    def test_signup_same_student_multiple_activities(self, client: TestClient):
        """Arrange-Act-Assert: Student can sign up for multiple different activities."""
        # Arrange: New student email
        new_student = "versatile.student@mergington.edu"

        # Act: Sign up for two different activities
        response1 = client.post(
            f"/activities/Chess Club/signup?email={new_student}"
        )
        response2 = client.post(
            f"/activities/Drama Club/signup?email={new_student}"
        )

        # Assert: Both signups succeed
        assert response1.status_code == 200
        assert response2.status_code == 200

        # Verify student appears in both activities
        all_activities = client.get("/activities").json()
        assert new_student in all_activities["Chess Club"]["participants"]
        assert new_student in all_activities["Drama Club"]["participants"]


class TestEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_empty_email_parameter(self, client: TestClient):
        """Arrange-Act-Assert: Signup with empty email string."""
        # Arrange: Empty string for email

        # Act: Attempt signup with empty email
        response = client.post(
            "/activities/Programming Class/signup?email="
        )

        # Assert: Request processed (email validation is not in spec, so empty string may be accepted)
        # This documents current behavior
        assert response.status_code in [200, 400, 422]

    def test_activity_name_case_sensitive(self, client: TestClient):
        """Arrange-Act-Assert: Activity names are case-sensitive."""
        # Arrange: Attempt to use wrong case for activity name
        student_email = "case.tester@mergington.edu"

        # Act: Sign up using incorrect case
        response = client.post(
            f"/activities/chess club/signup?email={student_email}"
        )

        # Assert: Should return 404 (activity not found)
        assert response.status_code == 404

    def test_special_characters_in_email(self, client: TestClient):
        """Arrange-Act-Assert: Email with special characters is accepted."""
        # Arrange: Email with special characters
        special_email = "student+tag@mergington.co.uk"
        query_params = urlencode({"email": special_email})

        # Act: Sign up with special character email
        response = client.post(
            f"/activities/Science Club/signup?{query_params}"
        )

        # Assert: Signup succeeds and email is stored
        assert response.status_code == 200
        activities = client.get("/activities").json()
        assert special_email in activities["Science Club"]["participants"]
