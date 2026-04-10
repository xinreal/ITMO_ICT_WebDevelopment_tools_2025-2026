from models import Organizer, ChallengeTask, Hackathon, HackathonFormat


organizer_1 = Organizer(
    id=1,
    full_name="Инга Семенова",
    email="inga.semen@example.com",
    phone="+79990000001",
    organization="ITMO"
)

organizer_2 = Organizer(
    id=2,
    full_name="Илья Бутусов",
    email="ilya0000@example.com",
    phone="+79993698187",
    organization="Tech City"
)

temp_organizers = [
    organizer_1.model_dump(mode="json"),
    organizer_2.model_dump(mode="json")
]

temp_hackathons = [
    Hackathon(
        id=1,
        title="AI Hackathon 2026",
        description="Хакатон по разработке ИИ-решений для образования.",
        city="Санкт-Петербург",
        format=HackathonFormat.hybrid,
        duration_hours=48,
        organizer=organizer_1,
        tasks=[
            ChallengeTask(
                id=1,
                title="Умный помощник для студентов",
                description="Разработать сервис, который помогает студентам искать учебные материалы.",
                requirements="Веб- или мобильный прототип, презентация решения.",
                evaluation_criteria="Полезность, качество идеи, удобство интерфейса."
            ),
            ChallengeTask(
                id=2,
                title="Аналитика успеваемости",
                description="Создать прототип системы анализа успеваемости студентов.",
                requirements="Дашборд или API, описание логики работы.",
                evaluation_criteria="Точность, наглядность, практическая применимость."
            )
        ]
    ).model_dump(mode="json"),

    Hackathon(
        id=2,
        title="GreenTech Sprint",
        description="Хакатон для экологических и городских цифровых решений.",
        city="Москва",
        format=HackathonFormat.offline,
        duration_hours=36,
        organizer=organizer_2,
        tasks=[
            ChallengeTask(
                id=3,
                title="Экологическая карта района",
                description="Сделать прототип карты с пунктами сортировки отходов.",
                requirements="Интерактивная карта, описание сценария использования.",
                evaluation_criteria="Актуальность, удобство, качество проработки."
            )
        ]
    ).model_dump(mode="json"),

    Hackathon(
        id=3,
        title="Startup Weekend",
        description="Короткий интенсив для разработки MVP стартап-идей.",
        city="Казань",
        format=HackathonFormat.online,
        duration_hours=24,
        organizer=organizer_1,
        tasks=[]
    ).model_dump(mode="json")
]