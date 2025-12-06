import json

import init_django_orm  # noqa: F401
from db.models import Race, Skill, Player, Guild


def main() -> None:
    with open("players.json") as f:
        players = json.load(f)

    for player, player_desc_dict in players.items():
        nickname = player
        email = player_desc_dict.get("email")
        bio = player_desc_dict.get("bio")

        race_data = player_desc_dict.get("race")
        if not race_data:
            raise ValueError(
                f"Player {nickname} has no race in input data"
            )
        if race_data:
            race_name = race_data.get("name")
            race_desc = race_data.get("description")

            race_obj, _ = Race.objects.get_or_create(
                name=race_name,
                defaults={
                    "description": race_desc
                },
            )

            skills = race_data.get("skills")
            if skills:
                for skill in skills:
                    skill_name = skill.get("name")
                    skill_bonus = skill.get("bonus")
                    Skill.objects.get_or_create(
                        name=skill_name,
                        defaults={
                            "bonus": skill_bonus,
                            "race": race_obj ,
                        },
                    )

        guild_obj = None
        guild_data = player_desc_dict.get("guild")
        if guild_data:
            guild_name = guild_data.get("name")
            guild_description = guild_data.get("description")
            guild_obj, _ = Guild.objects.get_or_create(
                name=guild_name,
                defaults={
                    "description": guild_description
                },
            )

        Player.objects.get_or_create(
            nickname=nickname,
            defaults={
                "email": email,
                "bio": bio,
                "race": race_obj,
                "guild": guild_obj,
            }
        )


if __name__ == "__main__":
    main()
