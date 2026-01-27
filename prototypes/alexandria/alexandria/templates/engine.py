"""
Template Engine - The constitution system.

Templates define the ESSENCE of things.
Instances are creations FROM templates.

Key concept:
- Templates are IMMUTABLE (the constitution)
- Instances are MUTABLE (your creation)
- You can CREATE from a template
- You cannot MODIFY a template

Example:
    Template: "House"
    - Must have: foundation, walls, roof
    - Can have: windows, doors, rooms
    - Style: any

    Instance: "My Modern House"
    - Has: foundation, walls, roof (required)
    - Has: 4 windows, 2 doors (optional)
    - Style: modern minimalist (your choice)

    You can change "My Modern House" freely.
    You cannot change what a "House" fundamentally is.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime
from enum import Enum
import hashlib
import json
import copy


class FieldType(Enum):
    """Types of template fields."""
    REQUIRED = "required"       # Must be provided
    OPTIONAL = "optional"       # Can be provided
    COMPUTED = "computed"       # Auto-generated
    REFERENCE = "reference"     # Reference to another template
    LIST = "list"               # List of items
    ENUM = "enum"               # One of predefined values


@dataclass
class TemplateField:
    """A field in a template."""
    name: str
    type: FieldType
    description: str
    default: Any = None
    choices: Optional[List[Any]] = None  # For enum fields
    validator: Optional[str] = None       # Validation rule
    immutable: bool = False               # Cannot be changed after creation


@dataclass
class Template:
    """
    An immutable template - the constitution.

    Templates define:
    - What fields are required
    - What fields are optional
    - What values are valid
    - The essence of the thing
    """
    name: str
    domain: str                          # Domain code (MATH, ART, etc.)
    description: str
    philosophy: str                      # The guiding principle
    fields: List[TemplateField]
    version: str = "1.0.0"
    created_at: str = ""
    checksum: str = ""                   # For integrity verification
    extends: Optional[str] = None        # Parent template
    tags: List[str] = field(default_factory=list)
    examples: List[Dict[str, Any]] = field(default_factory=list)

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.utcnow().isoformat()
        if not self.checksum:
            self.checksum = self._compute_checksum()

    def _compute_checksum(self) -> str:
        """Compute checksum for integrity."""
        content = f"{self.name}{self.domain}{self.version}"
        for f in self.fields:
            content += f"{f.name}{f.type.value}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def required_fields(self) -> List[TemplateField]:
        """Get required fields."""
        return [f for f in self.fields if f.type == FieldType.REQUIRED]

    def optional_fields(self) -> List[TemplateField]:
        """Get optional fields."""
        return [f for f in self.fields if f.type == FieldType.OPTIONAL]

    def validate(self, data: Dict[str, Any]) -> tuple:
        """
        Validate data against template.

        Returns: (is_valid, errors)
        """
        errors = []

        # Check required fields
        for f in self.required_fields():
            if f.name not in data or data[f.name] is None:
                errors.append(f"Missing required field: {f.name}")

        # Check enum values
        for f in self.fields:
            if f.type == FieldType.ENUM and f.name in data:
                if f.choices and data[f.name] not in f.choices:
                    errors.append(f"Invalid value for {f.name}: must be one of {f.choices}")

        return (len(errors) == 0, errors)


@dataclass
class Instance:
    """
    A mutable instance created from a template.

    Instances:
    - Are created FROM a template
    - Can be modified freely
    - Must satisfy template constraints
    - Track their history
    """
    id: str
    template_name: str
    template_checksum: str               # Links to specific template version
    data: Dict[str, Any]
    created_at: str = ""
    updated_at: str = ""
    created_by: str = ""                 # Agent or user
    history: List[Dict[str, Any]] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    locked_fields: List[str] = field(default_factory=list)  # Fields that can't change

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.utcnow().isoformat()
        if not self.updated_at:
            self.updated_at = self.created_at
        if not self.id:
            self.id = self._generate_id()

    def _generate_id(self) -> str:
        """Generate unique ID."""
        content = f"{self.template_name}{self.created_at}{json.dumps(self.data)}"
        return hashlib.sha256(content.encode()).hexdigest()[:12]

    def update(self, changes: Dict[str, Any], by: str = "unknown") -> bool:
        """
        Update instance data.

        Returns True if successful.
        Respects locked fields.
        """
        # Check locked fields
        for key in changes:
            if key in self.locked_fields:
                return False

        # Record history
        self.history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "by": by,
            "changes": changes,
            "previous": {k: self.data.get(k) for k in changes},
        })

        # Apply changes
        self.data.update(changes)
        self.updated_at = datetime.utcnow().isoformat()

        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "template": self.template_name,
            "data": self.data,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "created_by": self.created_by,
        }


# =============================================================================
# BUILT-IN TEMPLATES
# =============================================================================

TEMPLATES: List[Template] = [
    # =========================================================================
    # CREATIVE TEMPLATES
    # =========================================================================
    Template(
        name="house",
        domain="ART",
        description="A dwelling structure.",
        philosophy="A house is a machine for living in. But it's also a home.",
        fields=[
            TemplateField("foundation", FieldType.REQUIRED, "The base structure"),
            TemplateField("walls", FieldType.REQUIRED, "The enclosing walls"),
            TemplateField("roof", FieldType.REQUIRED, "The covering structure"),
            TemplateField("style", FieldType.OPTIONAL, "Architectural style", default="modern"),
            TemplateField("rooms", FieldType.LIST, "List of rooms"),
            TemplateField("windows", FieldType.OPTIONAL, "Number of windows", default=4),
            TemplateField("doors", FieldType.OPTIONAL, "Number of doors", default=2),
            TemplateField("color", FieldType.OPTIONAL, "Exterior color"),
            TemplateField("materials", FieldType.LIST, "Building materials"),
        ],
        examples=[
            {"foundation": "concrete", "walls": "brick", "roof": "shingle", "style": "colonial"},
            {"foundation": "concrete", "walls": "glass", "roof": "flat", "style": "modern"},
        ],
        tags=["building", "architecture", "dwelling"],
    ),
    Template(
        name="character",
        domain="WRIT",
        description="A fictional character.",
        philosophy="Characters are not described, they are revealed through action.",
        fields=[
            TemplateField("name", FieldType.REQUIRED, "Character name"),
            TemplateField("role", FieldType.REQUIRED, "Role in story", choices=["protagonist", "antagonist", "supporting", "background"]),
            TemplateField("motivation", FieldType.REQUIRED, "What drives them"),
            TemplateField("flaw", FieldType.REQUIRED, "Their key weakness"),
            TemplateField("backstory", FieldType.OPTIONAL, "Background history"),
            TemplateField("appearance", FieldType.OPTIONAL, "Physical description"),
            TemplateField("voice", FieldType.OPTIONAL, "How they speak"),
            TemplateField("relationships", FieldType.LIST, "Connections to other characters"),
            TemplateField("arc", FieldType.OPTIONAL, "Character development"),
        ],
        tags=["writing", "fiction", "storytelling"],
    ),
    Template(
        name="song",
        domain="MUS",
        description="A musical composition with lyrics.",
        philosophy="A good song is three chords and the truth.",
        fields=[
            TemplateField("title", FieldType.REQUIRED, "Song title"),
            TemplateField("key", FieldType.REQUIRED, "Musical key"),
            TemplateField("tempo", FieldType.REQUIRED, "BPM"),
            TemplateField("structure", FieldType.REQUIRED, "Song structure (e.g., ABABCB)"),
            TemplateField("verses", FieldType.LIST, "Verse lyrics"),
            TemplateField("chorus", FieldType.OPTIONAL, "Chorus lyrics"),
            TemplateField("bridge", FieldType.OPTIONAL, "Bridge section"),
            TemplateField("chord_progression", FieldType.LIST, "Chord sequence"),
            TemplateField("genre", FieldType.OPTIONAL, "Musical genre"),
            TemplateField("mood", FieldType.OPTIONAL, "Emotional tone"),
        ],
        tags=["music", "composition", "lyrics"],
    ),

    # =========================================================================
    # TECHNICAL TEMPLATES
    # =========================================================================
    Template(
        name="function",
        domain="CODE",
        description="A code function or method.",
        philosophy="A function should do one thing and do it well.",
        fields=[
            TemplateField("name", FieldType.REQUIRED, "Function name"),
            TemplateField("purpose", FieldType.REQUIRED, "What it does (one sentence)"),
            TemplateField("parameters", FieldType.LIST, "Input parameters"),
            TemplateField("returns", FieldType.REQUIRED, "Return type and meaning"),
            TemplateField("body", FieldType.REQUIRED, "Implementation"),
            TemplateField("examples", FieldType.LIST, "Usage examples"),
            TemplateField("errors", FieldType.LIST, "Possible errors"),
            TemplateField("complexity", FieldType.OPTIONAL, "Time/space complexity"),
        ],
        tags=["code", "programming", "function"],
    ),
    Template(
        name="api-endpoint",
        domain="CODE",
        description="A REST API endpoint.",
        philosophy="APIs should be predictable. Surprise is the enemy of usability.",
        fields=[
            TemplateField("path", FieldType.REQUIRED, "URL path"),
            TemplateField("method", FieldType.REQUIRED, "HTTP method", choices=["GET", "POST", "PUT", "PATCH", "DELETE"]),
            TemplateField("description", FieldType.REQUIRED, "What it does"),
            TemplateField("request_body", FieldType.OPTIONAL, "Request schema"),
            TemplateField("response", FieldType.REQUIRED, "Response schema"),
            TemplateField("errors", FieldType.LIST, "Error responses"),
            TemplateField("auth", FieldType.OPTIONAL, "Authentication required"),
            TemplateField("rate_limit", FieldType.OPTIONAL, "Rate limiting"),
        ],
        tags=["api", "rest", "endpoint"],
    ),

    # =========================================================================
    # SCIENCE TEMPLATES
    # =========================================================================
    Template(
        name="proof",
        domain="MATH",
        description="A mathematical proof.",
        philosophy="A proof is a logical argument that establishes truth beyond doubt.",
        fields=[
            TemplateField("theorem", FieldType.REQUIRED, "Statement to prove"),
            TemplateField("given", FieldType.REQUIRED, "Given information"),
            TemplateField("method", FieldType.REQUIRED, "Proof method", choices=["direct", "contradiction", "induction", "construction"]),
            TemplateField("steps", FieldType.LIST, "Proof steps"),
            TemplateField("conclusion", FieldType.REQUIRED, "QED statement"),
            TemplateField("corollaries", FieldType.LIST, "Derived results"),
            TemplateField("references", FieldType.LIST, "Cited theorems"),
        ],
        tags=["math", "proof", "theorem"],
    ),
    Template(
        name="experiment",
        domain="PHY",
        description="A scientific experiment.",
        philosophy="Experiment is the sole judge of scientific truth.",
        fields=[
            TemplateField("hypothesis", FieldType.REQUIRED, "What we're testing"),
            TemplateField("variables", FieldType.REQUIRED, "Independent and dependent variables"),
            TemplateField("controls", FieldType.REQUIRED, "Control conditions"),
            TemplateField("procedure", FieldType.LIST, "Step-by-step method"),
            TemplateField("data", FieldType.OPTIONAL, "Collected data"),
            TemplateField("analysis", FieldType.OPTIONAL, "Data analysis"),
            TemplateField("conclusion", FieldType.OPTIONAL, "Results interpretation"),
            TemplateField("errors", FieldType.LIST, "Sources of error"),
        ],
        tags=["science", "experiment", "research"],
    ),

    # =========================================================================
    # BUSINESS TEMPLATES
    # =========================================================================
    Template(
        name="campaign",
        domain="MKT",
        description="A marketing campaign.",
        philosophy="The best marketing doesn't feel like marketing.",
        fields=[
            TemplateField("name", FieldType.REQUIRED, "Campaign name"),
            TemplateField("objective", FieldType.REQUIRED, "Primary goal"),
            TemplateField("audience", FieldType.REQUIRED, "Target audience"),
            TemplateField("message", FieldType.REQUIRED, "Core message"),
            TemplateField("channels", FieldType.LIST, "Distribution channels"),
            TemplateField("budget", FieldType.OPTIONAL, "Budget allocation"),
            TemplateField("timeline", FieldType.OPTIONAL, "Campaign duration"),
            TemplateField("kpis", FieldType.LIST, "Success metrics"),
            TemplateField("assets", FieldType.LIST, "Creative assets"),
        ],
        tags=["marketing", "campaign", "advertising"],
    ),
    Template(
        name="email",
        domain="COMM",
        description="A professional email.",
        philosophy="Brevity is the soul of email. Get to the point.",
        fields=[
            TemplateField("subject", FieldType.REQUIRED, "Email subject line"),
            TemplateField("recipient", FieldType.REQUIRED, "Who it's for"),
            TemplateField("purpose", FieldType.REQUIRED, "Why you're writing"),
            TemplateField("body", FieldType.REQUIRED, "Email content"),
            TemplateField("call_to_action", FieldType.OPTIONAL, "What you want them to do"),
            TemplateField("tone", FieldType.OPTIONAL, "Formal/informal", choices=["formal", "casual", "urgent"]),
            TemplateField("attachments", FieldType.LIST, "Attached files"),
        ],
        tags=["communication", "email", "professional"],
    ),

    # =========================================================================
    # PERSONAL TEMPLATES
    # =========================================================================
    Template(
        name="journal",
        domain="PERS",
        description="A journal entry.",
        philosophy="Write to understand, not to remember.",
        fields=[
            TemplateField("date", FieldType.REQUIRED, "Entry date"),
            TemplateField("mood", FieldType.OPTIONAL, "How you feel"),
            TemplateField("events", FieldType.LIST, "What happened"),
            TemplateField("reflections", FieldType.OPTIONAL, "Thoughts and insights"),
            TemplateField("gratitude", FieldType.LIST, "Things to be grateful for"),
            TemplateField("tomorrow", FieldType.OPTIONAL, "Intentions for tomorrow"),
        ],
        tags=["personal", "journal", "reflection"],
    ),
    Template(
        name="goal",
        domain="PERS",
        description="A personal goal.",
        philosophy="A goal without a plan is just a wish.",
        fields=[
            TemplateField("goal", FieldType.REQUIRED, "What you want to achieve"),
            TemplateField("why", FieldType.REQUIRED, "Why it matters"),
            TemplateField("deadline", FieldType.OPTIONAL, "Target date"),
            TemplateField("milestones", FieldType.LIST, "Intermediate steps"),
            TemplateField("obstacles", FieldType.LIST, "Potential challenges"),
            TemplateField("resources", FieldType.LIST, "What you need"),
            TemplateField("progress", FieldType.OPTIONAL, "Current status"),
        ],
        tags=["personal", "goals", "planning"],
    ),
]


class TemplateEngine:
    """
    The template engine - creates instances from templates.

    Key operations:
    - Get template (read-only)
    - Create instance from template
    - Validate instance against template
    - Update instance (respecting constraints)
    """

    def __init__(self):
        """Initialize the engine."""
        self.templates = {t.name: t for t in TEMPLATES}
        self._instances: Dict[str, Instance] = {}

    def get_template(self, name: str) -> Optional[Template]:
        """Get a template by name (read-only)."""
        return self.templates.get(name)

    def list_templates(self, domain: Optional[str] = None) -> List[Template]:
        """List all templates, optionally filtered by domain."""
        if domain:
            return [t for t in TEMPLATES if t.domain == domain]
        return TEMPLATES

    def create(
        self,
        template_name: str,
        data: Dict[str, Any],
        created_by: str = "unknown",
    ) -> tuple:
        """
        Create an instance from a template.

        Returns: (instance, errors)
        """
        template = self.get_template(template_name)
        if not template:
            return (None, [f"Unknown template: {template_name}"])

        # Validate data
        is_valid, errors = template.validate(data)
        if not is_valid:
            return (None, errors)

        # Apply defaults
        full_data = copy.deepcopy(data)
        for field in template.fields:
            if field.name not in full_data and field.default is not None:
                full_data[field.name] = field.default

        # Create instance
        instance = Instance(
            id="",  # Will be generated
            template_name=template_name,
            template_checksum=template.checksum,
            data=full_data,
            created_by=created_by,
            locked_fields=[f.name for f in template.fields if f.immutable],
        )

        # Store instance
        self._instances[instance.id] = instance

        return (instance, [])

    def get_instance(self, instance_id: str) -> Optional[Instance]:
        """Get an instance by ID."""
        return self._instances.get(instance_id)

    def update_instance(
        self,
        instance_id: str,
        changes: Dict[str, Any],
        by: str = "unknown",
    ) -> tuple:
        """
        Update an instance.

        Returns: (success, errors)
        """
        instance = self.get_instance(instance_id)
        if not instance:
            return (False, ["Instance not found"])

        # Get template for validation
        template = self.get_template(instance.template_name)
        if not template:
            return (False, ["Template not found"])

        # Check locked fields
        locked_changes = [k for k in changes if k in instance.locked_fields]
        if locked_changes:
            return (False, [f"Cannot modify locked fields: {locked_changes}"])

        # Validate changes
        test_data = copy.deepcopy(instance.data)
        test_data.update(changes)
        is_valid, errors = template.validate(test_data)

        if not is_valid:
            return (False, errors)

        # Apply changes
        instance.update(changes, by=by)

        return (True, [])

    def validate_path_permission(
        self,
        template_name: str,
        operation: str,  # "read", "create", "update", "delete"
    ) -> bool:
        """
        Check if an operation is allowed on a template.

        Templates themselves are always read-only.
        Instances can be created, updated, deleted.
        """
        if operation == "read":
            return True

        # Templates are IMMUTABLE
        if template_name in self.templates:
            return operation in ("create",)  # Can only create instances

        return True  # Instances can be modified

    def stats(self) -> Dict[str, Any]:
        """Get engine statistics."""
        return {
            "total_templates": len(TEMPLATES),
            "total_instances": len(self._instances),
            "templates_by_domain": {
                domain: len([t for t in TEMPLATES if t.domain == domain])
                for domain in set(t.domain for t in TEMPLATES)
            },
        }
