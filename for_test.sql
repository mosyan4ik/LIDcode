PGDMP     4                     z         	   LIDcodeDB    14.3    14.3 �    =           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            >           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            ?           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            @           1262    16399 	   LIDcodeDB    DATABASE     h   CREATE DATABASE "LIDcodeDB" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'Russian_Russia.1251';
    DROP DATABASE "LIDcodeDB";
                LIDcode    false                        3079    16805    citext 	   EXTENSION     :   CREATE EXTENSION IF NOT EXISTS citext WITH SCHEMA public;
    DROP EXTENSION citext;
                   false            A           0    0    EXTENSION citext    COMMENT     S   COMMENT ON EXTENSION citext IS 'data type for case-insensitive character strings';
                        false    2            �            1259    16418    event    TABLE     [  CREATE TABLE public.event (
    id integer NOT NULL,
    name text NOT NULL,
    status text NOT NULL,
    description text,
    numberofparticipants integer,
    regulations text NOT NULL,
    "additionalMaterial" text NOT NULL,
    results text,
    materials text,
    "timeNow" time without time zone NOT NULL,
    image text,
    date_register timestamp with time zone,
    "date_closeRegister" timestamp with time zone,
    date_start timestamp with time zone,
    date_end timestamp with time zone,
    "timePublicationAdditionalMaterial" timestamp with time zone,
    "numberComands" integer
);
    DROP TABLE public.event;
       public         heap    LIDcode    false            �            1259    16421     event_id_seq    SEQUENCE     �   CREATE SEQUENCE public." event_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public." event_id_seq";
       public          LIDcode    false    214            B           0    0     event_id_seq    SEQUENCE OWNED BY     @   ALTER SEQUENCE public." event_id_seq" OWNED BY public.event.id;
          public          LIDcode    false    215            �            1259    16530 
   auth_group    TABLE     f   CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);
    DROP TABLE public.auth_group;
       public         heap    LIDcode    false            �            1259    16529    auth_group_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.auth_group_id_seq;
       public          LIDcode    false    231            C           0    0    auth_group_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;
          public          LIDcode    false    230            �            1259    16539    auth_group_permissions    TABLE     �   CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);
 *   DROP TABLE public.auth_group_permissions;
       public         heap    LIDcode    false            �            1259    16538    auth_group_permissions_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public.auth_group_permissions_id_seq;
       public          LIDcode    false    233            D           0    0    auth_group_permissions_id_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;
          public          LIDcode    false    232            �            1259    16523    auth_permission    TABLE     �   CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);
 #   DROP TABLE public.auth_permission;
       public         heap    LIDcode    false            �            1259    16522    auth_permission_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.auth_permission_id_seq;
       public          LIDcode    false    229            E           0    0    auth_permission_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;
          public          LIDcode    false    228            �            1259    16546 	   auth_user    TABLE     �  CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);
    DROP TABLE public.auth_user;
       public         heap    LIDcode    false            �            1259    16555    auth_user_groups    TABLE     ~   CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);
 $   DROP TABLE public.auth_user_groups;
       public         heap    LIDcode    false            �            1259    16554    auth_user_groups_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.auth_user_groups_id_seq;
       public          LIDcode    false    237            F           0    0    auth_user_groups_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;
          public          LIDcode    false    236            �            1259    16545    auth_user_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.auth_user_id_seq;
       public          LIDcode    false    235            G           0    0    auth_user_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;
          public          LIDcode    false    234            �            1259    16562    auth_user_user_permissions    TABLE     �   CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);
 .   DROP TABLE public.auth_user_user_permissions;
       public         heap    LIDcode    false            �            1259    16561 !   auth_user_user_permissions_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 8   DROP SEQUENCE public.auth_user_user_permissions_id_seq;
       public          LIDcode    false    239            H           0    0 !   auth_user_user_permissions_id_seq    SEQUENCE OWNED BY     g   ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;
          public          LIDcode    false    238            �            1259    16621    django_admin_log    TABLE     �  CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);
 $   DROP TABLE public.django_admin_log;
       public         heap    LIDcode    false            �            1259    16620    django_admin_log_id_seq    SEQUENCE     �   CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.django_admin_log_id_seq;
       public          LIDcode    false    241            I           0    0    django_admin_log_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;
          public          LIDcode    false    240            �            1259    16514    django_content_type    TABLE     �   CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);
 '   DROP TABLE public.django_content_type;
       public         heap    LIDcode    false            �            1259    16513    django_content_type_id_seq    SEQUENCE     �   CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.django_content_type_id_seq;
       public          LIDcode    false    227            J           0    0    django_content_type_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;
          public          LIDcode    false    226            �            1259    16505    django_migrations    TABLE     �   CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);
 %   DROP TABLE public.django_migrations;
       public         heap    LIDcode    false            �            1259    16504    django_migrations_id_seq    SEQUENCE     �   CREATE SEQUENCE public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.django_migrations_id_seq;
       public          LIDcode    false    225            K           0    0    django_migrations_id_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;
          public          LIDcode    false    224            �            1259    16650    django_session    TABLE     �   CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);
 "   DROP TABLE public.django_session;
       public         heap    LIDcode    false            �            1259    16474    event_organizers    TABLE     �   CREATE TABLE public.event_organizers (
    event_id integer NOT NULL,
    organizers_id integer NOT NULL,
    id integer NOT NULL
);
 $   DROP TABLE public.event_organizers;
       public         heap    LIDcode    false            �            1259    16787    event_organizers_id_seq    SEQUENCE     �   CREATE SEQUENCE public.event_organizers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.event_organizers_id_seq;
       public          LIDcode    false    222            L           0    0    event_organizers_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.event_organizers_id_seq OWNED BY public.event_organizers.id;
          public          LIDcode    false    243            �            1259    16984    event_participants    TABLE     �   CREATE TABLE public.event_participants (
    id integer NOT NULL,
    team_id integer NOT NULL,
    event_id integer NOT NULL
);
 &   DROP TABLE public.event_participants;
       public         heap    LIDcode    false            �            1259    16983    event_participants_id_seq    SEQUENCE     �   CREATE SEQUENCE public.event_participants_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public.event_participants_id_seq;
       public          LIDcode    false    250            M           0    0    event_participants_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public.event_participants_id_seq OWNED BY public.event_participants.id;
          public          LIDcode    false    249            �            1259    16489    event_sponsors    TABLE     �   CREATE TABLE public.event_sponsors (
    event_id integer NOT NULL,
    sponsors_id integer NOT NULL,
    id integer NOT NULL
);
 "   DROP TABLE public.event_sponsors;
       public         heap    LIDcode    false            �            1259    16794    event_sponsors_id_seq    SEQUENCE     �   CREATE SEQUENCE public.event_sponsors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.event_sponsors_id_seq;
       public          LIDcode    false    223            N           0    0    event_sponsors_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.event_sponsors_id_seq OWNED BY public.event_sponsors.id;
          public          LIDcode    false    244            �            1259    16911    mainList_participant    TABLE     J  CREATE TABLE public."mainList_participant" (
    id bigint NOT NULL,
    name public.citext NOT NULL,
    emailadress public.citext NOT NULL,
    phonenumber public.citext NOT NULL,
    organization public.citext NOT NULL,
    university public.citext,
    university_faculty public.citext,
    university_course public.citext
);
 *   DROP TABLE public."mainList_participant";
       public         heap    LIDcode    false    2    2    2    2    2    2    2    2    2    2    2    2    2    2    2    2    2    2    2    2    2    2    2    2    2    2    2    2    2    2    2    2    2    2    2            �            1259    16910    mainList_participant_id_seq    SEQUENCE     �   CREATE SEQUENCE public."mainList_participant_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public."mainList_participant_id_seq";
       public          LIDcode    false    246            O           0    0    mainList_participant_id_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public."mainList_participant_id_seq" OWNED BY public."mainList_participant".id;
          public          LIDcode    false    245            �            1259    16428 
   organizers    TABLE     |   CREATE TABLE public.organizers (
    id integer NOT NULL,
    name text NOT NULL,
    link text NOT NULL,
    image text
);
    DROP TABLE public.organizers;
       public         heap    LIDcode    false            �            1259    16439    organizers_id_seq    SEQUENCE     �   CREATE SEQUENCE public.organizers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.organizers_id_seq;
       public          LIDcode    false    216            P           0    0    organizers_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.organizers_id_seq OWNED BY public.organizers.id;
          public          LIDcode    false    219            �            1259    16401    participant    TABLE       CREATE TABLE public.participant (
    emailadress text NOT NULL,
    phonenumber text NOT NULL,
    organization text NOT NULL,
    university_faculty text,
    university_course text,
    id integer NOT NULL,
    name text,
    iscoach boolean,
    "iscontactFace" boolean
);
    DROP TABLE public.participant;
       public         heap    LIDcode    false            �            1259    16400    participant_id_seq    SEQUENCE     �   CREATE SEQUENCE public.participant_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.participant_id_seq;
       public          LIDcode    false    211            Q           0    0    participant_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.participant_id_seq OWNED BY public.participant.id;
          public          LIDcode    false    210            �            1259    16454    requests    TABLE     w   CREATE TABLE public.requests (
    id integer NOT NULL,
    event_id integer NOT NULL,
    team_id integer NOT NULL
);
    DROP TABLE public.requests;
       public         heap    LIDcode    false            �            1259    16457    requests_id_seq    SEQUENCE     �   CREATE SEQUENCE public.requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.requests_id_seq;
       public          LIDcode    false    220            R           0    0    requests_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.requests_id_seq OWNED BY public.requests.id;
          public          LIDcode    false    221            �            1259    16431    sponsors    TABLE     z   CREATE TABLE public.sponsors (
    id integer NOT NULL,
    name text NOT NULL,
    link text NOT NULL,
    image text
);
    DROP TABLE public.sponsors;
       public         heap    LIDcode    false            �            1259    16434    sponsors_id_seq    SEQUENCE     �   CREATE SEQUENCE public.sponsors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.sponsors_id_seq;
       public          LIDcode    false    217            S           0    0    sponsors_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.sponsors_id_seq OWNED BY public.sponsors.id;
          public          LIDcode    false    218            �            1259    16410    team    TABLE     �   CREATE TABLE public.team (
    id integer NOT NULL,
    coach_id integer NOT NULL,
    "contactPerson_id" integer NOT NULL,
    name text NOT NULL,
    "teamMembers" integer,
    approvement text,
    my_event_id integer
);
    DROP TABLE public.team;
       public         heap    LIDcode    false            �            1259    16409    team_id_seq    SEQUENCE     �   CREATE SEQUENCE public.team_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 "   DROP SEQUENCE public.team_id_seq;
       public          LIDcode    false    213            T           0    0    team_id_seq    SEQUENCE OWNED BY     ;   ALTER SEQUENCE public.team_id_seq OWNED BY public.team.id;
          public          LIDcode    false    212            �            1259    16963    team_teamMembers    TABLE     �   CREATE TABLE public."team_teamMembers" (
    id integer NOT NULL,
    participant_id integer NOT NULL,
    team_id integer NOT NULL
);
 &   DROP TABLE public."team_teamMembers";
       public         heap    LIDcode    false            �            1259    16966    team_teamMembers_id_seq    SEQUENCE     �   CREATE SEQUENCE public."team_teamMembers_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public."team_teamMembers_id_seq";
       public          LIDcode    false    247            U           0    0    team_teamMembers_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public."team_teamMembers_id_seq" OWNED BY public."team_teamMembers".id;
          public          LIDcode    false    248            %           2604    16533    auth_group id    DEFAULT     n   ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);
 <   ALTER TABLE public.auth_group ALTER COLUMN id DROP DEFAULT;
       public          LIDcode    false    231    230    231            &           2604    16542    auth_group_permissions id    DEFAULT     �   ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);
 H   ALTER TABLE public.auth_group_permissions ALTER COLUMN id DROP DEFAULT;
       public          LIDcode    false    232    233    233            $           2604    16526    auth_permission id    DEFAULT     x   ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);
 A   ALTER TABLE public.auth_permission ALTER COLUMN id DROP DEFAULT;
       public          LIDcode    false    228    229    229            '           2604    16549    auth_user id    DEFAULT     l   ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);
 ;   ALTER TABLE public.auth_user ALTER COLUMN id DROP DEFAULT;
       public          LIDcode    false    235    234    235            (           2604    16558    auth_user_groups id    DEFAULT     z   ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);
 B   ALTER TABLE public.auth_user_groups ALTER COLUMN id DROP DEFAULT;
       public          LIDcode    false    236    237    237            )           2604    16565    auth_user_user_permissions id    DEFAULT     �   ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);
 L   ALTER TABLE public.auth_user_user_permissions ALTER COLUMN id DROP DEFAULT;
       public          LIDcode    false    238    239    239            *           2604    16624    django_admin_log id    DEFAULT     z   ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);
 B   ALTER TABLE public.django_admin_log ALTER COLUMN id DROP DEFAULT;
       public          LIDcode    false    240    241    241            #           2604    16517    django_content_type id    DEFAULT     �   ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);
 E   ALTER TABLE public.django_content_type ALTER COLUMN id DROP DEFAULT;
       public          LIDcode    false    226    227    227            "           2604    16508    django_migrations id    DEFAULT     |   ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);
 C   ALTER TABLE public.django_migrations ALTER COLUMN id DROP DEFAULT;
       public          LIDcode    false    224    225    225                       2604    16422    event id    DEFAULT     g   ALTER TABLE ONLY public.event ALTER COLUMN id SET DEFAULT nextval('public." event_id_seq"'::regclass);
 7   ALTER TABLE public.event ALTER COLUMN id DROP DEFAULT;
       public          LIDcode    false    215    214                        2604    16788    event_organizers id    DEFAULT     z   ALTER TABLE ONLY public.event_organizers ALTER COLUMN id SET DEFAULT nextval('public.event_organizers_id_seq'::regclass);
 B   ALTER TABLE public.event_organizers ALTER COLUMN id DROP DEFAULT;
       public          LIDcode    false    243    222            .           2604    16987    event_participants id    DEFAULT     ~   ALTER TABLE ONLY public.event_participants ALTER COLUMN id SET DEFAULT nextval('public.event_participants_id_seq'::regclass);
 D   ALTER TABLE public.event_participants ALTER COLUMN id DROP DEFAULT;
       public          LIDcode    false    249    250    250            !           2604    16795    event_sponsors id    DEFAULT     v   ALTER TABLE ONLY public.event_sponsors ALTER COLUMN id SET DEFAULT nextval('public.event_sponsors_id_seq'::regclass);
 @   ALTER TABLE public.event_sponsors ALTER COLUMN id DROP DEFAULT;
       public          LIDcode    false    244    223            ,           2604    16914    mainList_participant id    DEFAULT     �   ALTER TABLE ONLY public."mainList_participant" ALTER COLUMN id SET DEFAULT nextval('public."mainList_participant_id_seq"'::regclass);
 H   ALTER TABLE public."mainList_participant" ALTER COLUMN id DROP DEFAULT;
       public          LIDcode    false    246    245    246                       2604    16440    organizers id    DEFAULT     n   ALTER TABLE ONLY public.organizers ALTER COLUMN id SET DEFAULT nextval('public.organizers_id_seq'::regclass);
 <   ALTER TABLE public.organizers ALTER COLUMN id DROP DEFAULT;
       public          LIDcode    false    219    216                       2604    16404    participant id    DEFAULT     p   ALTER TABLE ONLY public.participant ALTER COLUMN id SET DEFAULT nextval('public.participant_id_seq'::regclass);
 =   ALTER TABLE public.participant ALTER COLUMN id DROP DEFAULT;
       public          LIDcode    false    210    211    211                       2604    16458    requests id    DEFAULT     j   ALTER TABLE ONLY public.requests ALTER COLUMN id SET DEFAULT nextval('public.requests_id_seq'::regclass);
 :   ALTER TABLE public.requests ALTER COLUMN id DROP DEFAULT;
       public          LIDcode    false    221    220                       2604    16435    sponsors id    DEFAULT     j   ALTER TABLE ONLY public.sponsors ALTER COLUMN id SET DEFAULT nextval('public.sponsors_id_seq'::regclass);
 :   ALTER TABLE public.sponsors ALTER COLUMN id DROP DEFAULT;
       public          LIDcode    false    218    217                       2604    16413    team id    DEFAULT     b   ALTER TABLE ONLY public.team ALTER COLUMN id SET DEFAULT nextval('public.team_id_seq'::regclass);
 6   ALTER TABLE public.team ALTER COLUMN id DROP DEFAULT;
       public          LIDcode    false    213    212    213            -           2604    16967    team_teamMembers id    DEFAULT     ~   ALTER TABLE ONLY public."team_teamMembers" ALTER COLUMN id SET DEFAULT nextval('public."team_teamMembers_id_seq"'::regclass);
 D   ALTER TABLE public."team_teamMembers" ALTER COLUMN id DROP DEFAULT;
       public          LIDcode    false    248    247            '          0    16530 
   auth_group 
   TABLE DATA           .   COPY public.auth_group (id, name) FROM stdin;
    public          LIDcode    false    231   [�       )          0    16539    auth_group_permissions 
   TABLE DATA           M   COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
    public          LIDcode    false    233   x�       %          0    16523    auth_permission 
   TABLE DATA           N   COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
    public          LIDcode    false    229   ��       +          0    16546 	   auth_user 
   TABLE DATA           �   COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
    public          LIDcode    false    235   ��       -          0    16555    auth_user_groups 
   TABLE DATA           A   COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
    public          LIDcode    false    237   F�       /          0    16562    auth_user_user_permissions 
   TABLE DATA           P   COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
    public          LIDcode    false    239   c�       1          0    16621    django_admin_log 
   TABLE DATA           �   COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
    public          LIDcode    false    241   ��       #          0    16514    django_content_type 
   TABLE DATA           C   COPY public.django_content_type (id, app_label, model) FROM stdin;
    public          LIDcode    false    227   �      !          0    16505    django_migrations 
   TABLE DATA           C   COPY public.django_migrations (id, app, name, applied) FROM stdin;
    public          LIDcode    false    225         2          0    16650    django_session 
   TABLE DATA           P   COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
    public          LIDcode    false    242   �                0    16418    event 
   TABLE DATA             COPY public.event (id, name, status, description, numberofparticipants, regulations, "additionalMaterial", results, materials, "timeNow", image, date_register, "date_closeRegister", date_start, date_end, "timePublicationAdditionalMaterial", "numberComands") FROM stdin;
    public          LIDcode    false    214   D                0    16474    event_organizers 
   TABLE DATA           G   COPY public.event_organizers (event_id, organizers_id, id) FROM stdin;
    public          LIDcode    false    222   l)      :          0    16984    event_participants 
   TABLE DATA           C   COPY public.event_participants (id, team_id, event_id) FROM stdin;
    public          LIDcode    false    250   �)                0    16489    event_sponsors 
   TABLE DATA           C   COPY public.event_sponsors (event_id, sponsors_id, id) FROM stdin;
    public          LIDcode    false    223   �)      6          0    16911    mainList_participant 
   TABLE DATA           �   COPY public."mainList_participant" (id, name, emailadress, phonenumber, organization, university, university_faculty, university_course) FROM stdin;
    public          LIDcode    false    246   *                0    16428 
   organizers 
   TABLE DATA           ;   COPY public.organizers (id, name, link, image) FROM stdin;
    public          LIDcode    false    216   "*                0    16401    participant 
   TABLE DATA           �   COPY public.participant (emailadress, phonenumber, organization, university_faculty, university_course, id, name, iscoach, "iscontactFace") FROM stdin;
    public          LIDcode    false    211   +                0    16454    requests 
   TABLE DATA           9   COPY public.requests (id, event_id, team_id) FROM stdin;
    public          LIDcode    false    220   .,                0    16431    sponsors 
   TABLE DATA           9   COPY public.sponsors (id, name, link, image) FROM stdin;
    public          LIDcode    false    217   K,                0    16410    team 
   TABLE DATA           o   COPY public.team (id, coach_id, "contactPerson_id", name, "teamMembers", approvement, my_event_id) FROM stdin;
    public          LIDcode    false    213   -      7          0    16963    team_teamMembers 
   TABLE DATA           I   COPY public."team_teamMembers" (id, participant_id, team_id) FROM stdin;
    public          LIDcode    false    247   �-      V           0    0     event_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public." event_id_seq"', 15, true);
          public          LIDcode    false    215            W           0    0    auth_group_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);
          public          LIDcode    false    230            X           0    0    auth_group_permissions_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);
          public          LIDcode    false    232            Y           0    0    auth_permission_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.auth_permission_id_seq', 48, true);
          public          LIDcode    false    228            Z           0    0    auth_user_groups_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);
          public          LIDcode    false    236            [           0    0    auth_user_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.auth_user_id_seq', 1, true);
          public          LIDcode    false    234            \           0    0 !   auth_user_user_permissions_id_seq    SEQUENCE SET     P   SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);
          public          LIDcode    false    238            ]           0    0    django_admin_log_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.django_admin_log_id_seq', 543, true);
          public          LIDcode    false    240            ^           0    0    django_content_type_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.django_content_type_id_seq', 12, true);
          public          LIDcode    false    226            _           0    0    django_migrations_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.django_migrations_id_seq', 31, true);
          public          LIDcode    false    224            `           0    0    event_organizers_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.event_organizers_id_seq', 3, true);
          public          LIDcode    false    243            a           0    0    event_participants_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.event_participants_id_seq', 17, true);
          public          LIDcode    false    249            b           0    0    event_sponsors_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.event_sponsors_id_seq', 7, true);
          public          LIDcode    false    244            c           0    0    mainList_participant_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public."mainList_participant_id_seq"', 1, false);
          public          LIDcode    false    245            d           0    0    organizers_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.organizers_id_seq', 3, true);
          public          LIDcode    false    219            e           0    0    participant_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.participant_id_seq', 178, true);
          public          LIDcode    false    210            f           0    0    requests_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.requests_id_seq', 1, false);
          public          LIDcode    false    221            g           0    0    sponsors_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.sponsors_id_seq', 13, true);
          public          LIDcode    false    218            h           0    0    team_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.team_id_seq', 137, true);
          public          LIDcode    false    212            i           0    0    team_teamMembers_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public."team_teamMembers_id_seq"', 141, true);
          public          LIDcode    false    248            4           2606    16453    event _event_pk 
   CONSTRAINT     M   ALTER TABLE ONLY public.event
    ADD CONSTRAINT _event_pk PRIMARY KEY (id);
 9   ALTER TABLE ONLY public.event DROP CONSTRAINT _event_pk;
       public            LIDcode    false    214            L           2606    16648    auth_group auth_group_name_key 
   CONSTRAINT     Y   ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);
 H   ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_name_key;
       public            LIDcode    false    231            Q           2606    16578 R   auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);
 |   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
       public            LIDcode    false    233    233            T           2606    16544 2   auth_group_permissions auth_group_permissions_pkey 
   CONSTRAINT     p   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);
 \   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_pkey;
       public            LIDcode    false    233            N           2606    16535    auth_group auth_group_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_pkey;
       public            LIDcode    false    231            G           2606    16569 F   auth_permission auth_permission_content_type_id_codename_01ab375a_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);
 p   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq;
       public            LIDcode    false    229    229            I           2606    16528 $   auth_permission auth_permission_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_pkey;
       public            LIDcode    false    229            \           2606    16560 &   auth_user_groups auth_user_groups_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_pkey;
       public            LIDcode    false    237            _           2606    16593 @   auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);
 j   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq;
       public            LIDcode    false    237    237            V           2606    16551    auth_user auth_user_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.auth_user DROP CONSTRAINT auth_user_pkey;
       public            LIDcode    false    235            b           2606    16567 :   auth_user_user_permissions auth_user_user_permissions_pkey 
   CONSTRAINT     x   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);
 d   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_pkey;
       public            LIDcode    false    239            e           2606    16607 Y   auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);
 �   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq;
       public            LIDcode    false    239    239            Y           2606    16643     auth_user auth_user_username_key 
   CONSTRAINT     _   ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);
 J   ALTER TABLE ONLY public.auth_user DROP CONSTRAINT auth_user_username_key;
       public            LIDcode    false    235            h           2606    16629 &   django_admin_log django_admin_log_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_pkey;
       public            LIDcode    false    241            B           2606    16521 E   django_content_type django_content_type_app_label_model_76bd3d3b_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);
 o   ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq;
       public            LIDcode    false    227    227            D           2606    16519 ,   django_content_type django_content_type_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);
 V   ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_pkey;
       public            LIDcode    false    227            @           2606    16512 (   django_migrations django_migrations_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.django_migrations DROP CONSTRAINT django_migrations_pkey;
       public            LIDcode    false    225            l           2606    16656 "   django_session django_session_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);
 L   ALTER TABLE ONLY public.django_session DROP CONSTRAINT django_session_pkey;
       public            LIDcode    false    242            <           2606    16793 $   event_organizers event_organizers_pk 
   CONSTRAINT     b   ALTER TABLE ONLY public.event_organizers
    ADD CONSTRAINT event_organizers_pk PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.event_organizers DROP CONSTRAINT event_organizers_pk;
       public            LIDcode    false    222            s           2606    16989 (   event_participants event_participants_pk 
   CONSTRAINT     f   ALTER TABLE ONLY public.event_participants
    ADD CONSTRAINT event_participants_pk PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.event_participants DROP CONSTRAINT event_participants_pk;
       public            LIDcode    false    250            >           2606    16800     event_sponsors event_sponsors_pk 
   CONSTRAINT     ^   ALTER TABLE ONLY public.event_sponsors
    ADD CONSTRAINT event_sponsors_pk PRIMARY KEY (id);
 J   ALTER TABLE ONLY public.event_sponsors DROP CONSTRAINT event_sponsors_pk;
       public            LIDcode    false    223            o           2606    16918 .   mainList_participant mainList_participant_pkey 
   CONSTRAINT     p   ALTER TABLE ONLY public."mainList_participant"
    ADD CONSTRAINT "mainList_participant_pkey" PRIMARY KEY (id);
 \   ALTER TABLE ONLY public."mainList_participant" DROP CONSTRAINT "mainList_participant_pkey";
       public            LIDcode    false    246            6           2606    16447    organizers organizers_pk 
   CONSTRAINT     V   ALTER TABLE ONLY public.organizers
    ADD CONSTRAINT organizers_pk PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.organizers DROP CONSTRAINT organizers_pk;
       public            LIDcode    false    216            0           2606    16408    participant participant_pk 
   CONSTRAINT     X   ALTER TABLE ONLY public.participant
    ADD CONSTRAINT participant_pk PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.participant DROP CONSTRAINT participant_pk;
       public            LIDcode    false    211            :           2606    16463    requests requests_pk 
   CONSTRAINT     R   ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_pk PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.requests DROP CONSTRAINT requests_pk;
       public            LIDcode    false    220            8           2606    16451    sponsors sponsors_pk 
   CONSTRAINT     R   ALTER TABLE ONLY public.sponsors
    ADD CONSTRAINT sponsors_pk PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.sponsors DROP CONSTRAINT sponsors_pk;
       public            LIDcode    false    217            2           2606    16415    team team_pk 
   CONSTRAINT     J   ALTER TABLE ONLY public.team
    ADD CONSTRAINT team_pk PRIMARY KEY (id);
 6   ALTER TABLE ONLY public.team DROP CONSTRAINT team_pk;
       public            LIDcode    false    213            q           2606    16972 $   team_teamMembers team_teammembers_pk 
   CONSTRAINT     d   ALTER TABLE ONLY public."team_teamMembers"
    ADD CONSTRAINT team_teammembers_pk PRIMARY KEY (id);
 P   ALTER TABLE ONLY public."team_teamMembers" DROP CONSTRAINT team_teammembers_pk;
       public            LIDcode    false    247            J           1259    16649    auth_group_name_a6ea08ec_like    INDEX     h   CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);
 1   DROP INDEX public.auth_group_name_a6ea08ec_like;
       public            LIDcode    false    231            O           1259    16589 (   auth_group_permissions_group_id_b120cbf9    INDEX     o   CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);
 <   DROP INDEX public.auth_group_permissions_group_id_b120cbf9;
       public            LIDcode    false    233            R           1259    16590 -   auth_group_permissions_permission_id_84c5c92e    INDEX     y   CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);
 A   DROP INDEX public.auth_group_permissions_permission_id_84c5c92e;
       public            LIDcode    false    233            E           1259    16575 (   auth_permission_content_type_id_2f476e4b    INDEX     o   CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);
 <   DROP INDEX public.auth_permission_content_type_id_2f476e4b;
       public            LIDcode    false    229            Z           1259    16605 "   auth_user_groups_group_id_97559544    INDEX     c   CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);
 6   DROP INDEX public.auth_user_groups_group_id_97559544;
       public            LIDcode    false    237            ]           1259    16604 !   auth_user_groups_user_id_6a12ed8b    INDEX     a   CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);
 5   DROP INDEX public.auth_user_groups_user_id_6a12ed8b;
       public            LIDcode    false    237            `           1259    16619 1   auth_user_user_permissions_permission_id_1fbb5f2c    INDEX     �   CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);
 E   DROP INDEX public.auth_user_user_permissions_permission_id_1fbb5f2c;
       public            LIDcode    false    239            c           1259    16618 +   auth_user_user_permissions_user_id_a95ead1b    INDEX     u   CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);
 ?   DROP INDEX public.auth_user_user_permissions_user_id_a95ead1b;
       public            LIDcode    false    239            W           1259    16644     auth_user_username_6821ab7c_like    INDEX     n   CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);
 4   DROP INDEX public.auth_user_username_6821ab7c_like;
       public            LIDcode    false    235            f           1259    16640 )   django_admin_log_content_type_id_c4bce8eb    INDEX     q   CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);
 =   DROP INDEX public.django_admin_log_content_type_id_c4bce8eb;
       public            LIDcode    false    241            i           1259    16641 !   django_admin_log_user_id_c564eba6    INDEX     a   CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);
 5   DROP INDEX public.django_admin_log_user_id_c564eba6;
       public            LIDcode    false    241            j           1259    16658 #   django_session_expire_date_a5c62663    INDEX     e   CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);
 7   DROP INDEX public.django_session_expire_date_a5c62663;
       public            LIDcode    false    242            m           1259    16657 (   django_session_session_key_c0390e0f_like    INDEX     ~   CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);
 <   DROP INDEX public.django_session_session_key_c0390e0f_like;
       public            LIDcode    false    242            |           2606    16584 O   auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
 y   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
       public          LIDcode    false    3401    229    233            {           2606    16579 P   auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;
 z   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
       public          LIDcode    false    233    231    3406            z           2606    16570 E   auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
 o   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co;
       public          LIDcode    false    227    3396    229            ~           2606    16599 D   auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;
 n   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id;
       public          LIDcode    false    3406    237    231            }           2606    16594 B   auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 l   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id;
       public          LIDcode    false    235    3414    237            �           2606    16613 S   auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
 }   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm;
       public          LIDcode    false    239    3401    229                       2606    16608 V   auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id;
       public          LIDcode    false    235    3414    239            �           2606    16630 G   django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co    FK CONSTRAINT     �   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
 q   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co;
       public          LIDcode    false    241    3396    227            �           2606    16635 B   django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 l   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id;
       public          LIDcode    false    241    235    3414            v           2606    16479 $   event_organizers event_organizers_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.event_organizers
    ADD CONSTRAINT event_organizers_fk FOREIGN KEY (organizers_id) REFERENCES public.organizers(id) ON DELETE CASCADE;
 N   ALTER TABLE ONLY public.event_organizers DROP CONSTRAINT event_organizers_fk;
       public          LIDcode    false    3382    222    216            w           2606    16484 &   event_organizers event_organizers_fk_1    FK CONSTRAINT     �   ALTER TABLE ONLY public.event_organizers
    ADD CONSTRAINT event_organizers_fk_1 FOREIGN KEY (event_id) REFERENCES public.event(id) ON DELETE CASCADE;
 P   ALTER TABLE ONLY public.event_organizers DROP CONSTRAINT event_organizers_fk_1;
       public          LIDcode    false    222    3380    214            �           2606    16990 (   event_participants event_participants_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.event_participants
    ADD CONSTRAINT event_participants_fk FOREIGN KEY (team_id) REFERENCES public.team(id);
 R   ALTER TABLE ONLY public.event_participants DROP CONSTRAINT event_participants_fk;
       public          LIDcode    false    250    3378    213            �           2606    16995 *   event_participants event_participants_fk_1    FK CONSTRAINT     �   ALTER TABLE ONLY public.event_participants
    ADD CONSTRAINT event_participants_fk_1 FOREIGN KEY (event_id) REFERENCES public.event(id);
 T   ALTER TABLE ONLY public.event_participants DROP CONSTRAINT event_participants_fk_1;
       public          LIDcode    false    250    214    3380            x           2606    16494     event_sponsors event_sponsors_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.event_sponsors
    ADD CONSTRAINT event_sponsors_fk FOREIGN KEY (sponsors_id) REFERENCES public.sponsors(id) ON DELETE CASCADE;
 J   ALTER TABLE ONLY public.event_sponsors DROP CONSTRAINT event_sponsors_fk;
       public          LIDcode    false    3384    223    217            y           2606    16499 "   event_sponsors event_sponsors_fk_1    FK CONSTRAINT     �   ALTER TABLE ONLY public.event_sponsors
    ADD CONSTRAINT event_sponsors_fk_1 FOREIGN KEY (event_id) REFERENCES public.event(id) ON DELETE CASCADE;
 L   ALTER TABLE ONLY public.event_sponsors DROP CONSTRAINT event_sponsors_fk_1;
       public          LIDcode    false    214    223    3380            t           2606    16464    requests requests_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_fk FOREIGN KEY (event_id) REFERENCES public.event(id) ON DELETE CASCADE;
 >   ALTER TABLE ONLY public.requests DROP CONSTRAINT requests_fk;
       public          LIDcode    false    214    3380    220            u           2606    16469    requests requests_fk_1    FK CONSTRAINT     �   ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_fk_1 FOREIGN KEY (team_id) REFERENCES public.team(id) ON DELETE CASCADE;
 @   ALTER TABLE ONLY public.requests DROP CONSTRAINT requests_fk_1;
       public          LIDcode    false    220    3378    213            �           2606    16973 $   team_teamMembers team_teammembers_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public."team_teamMembers"
    ADD CONSTRAINT team_teammembers_fk FOREIGN KEY (team_id) REFERENCES public.team(id);
 P   ALTER TABLE ONLY public."team_teamMembers" DROP CONSTRAINT team_teammembers_fk;
       public          LIDcode    false    213    3378    247            �           2606    16978 &   team_teamMembers team_teammembers_fk_1    FK CONSTRAINT     �   ALTER TABLE ONLY public."team_teamMembers"
    ADD CONSTRAINT team_teammembers_fk_1 FOREIGN KEY (participant_id) REFERENCES public.participant(id);
 R   ALTER TABLE ONLY public."team_teamMembers" DROP CONSTRAINT team_teammembers_fk_1;
       public          LIDcode    false    247    211    3376            '      x������ � �      )      x������ � �      %   �  x�e��m�0F�����l���5
F"�R۰��(�"������P�H:7�| ����n��8uǅk��j�	��p�#������K��ɍ�%+/��Pؽ��*��nxo�o����XK9��`7�O�$(�-+*�˖ǡ;��DA���r�O^�X��!�`����lp�n0
�?�Vr>ui|Vr:4<k�Mm��<yߵc���x�Y����[)2�IH�;�5��O�Œ5g4�*�fk�⭮Q�NP��3C�Sig��2&��Ze���.A�l���PO}r!D�:!�A��sЁڜ�n8�m��o���(U�IBV�V0�IXd\�()AN���w����#�*��J�A�~�+̠���K�oC_c�o�:������%(�6���jI^mÌO/��+�3:�^��m]�nl|���P�EHm��ځD�R$D�S%b��?}M��t�~���fl�=<TjI�`�����؋G4�zxy��A��      +   �   x�5ʻ�0@�<ڟR�����xAcb��ED�oo�Y?�ڤJ3��� �.`��;�����ޛ�,�ױ���|�&����3�B8e�?�$')E-E3�_��(��)`af�D'P/p���jbH���A�A��t�V���r_a�jk���,�      -      x������ � �      /      x������ � �      1      x��][�d�q~����%7��X�4� y����6��fV�x-);+!�a�� 6  �<`�@�am%�e��B�?
����!���hvzf����β�.��E�X�T�_P��N�V�W�e�����8��w�~�����o���o<;�#���ӯ}��ó�����~�{�8�'��Xf��
�>���T��`��,�e�����خt����c%=x#��a�ը���a��_�w�ֳݭa�����`��PPA$m-iW�����O%�!@�r+̓VΓ� � ��o��<z|���"��k���w����=����MC������#~�����(��eW���Rx�B��l��o�U�?ډ��O���S�ߨQ��K&P3����T]]-�E�Ps��� ��8.�acFQ�D���Ɏ��yel)+A��[\"�+Q�UBWHaT��s��
��H��I+�`*Xr�\�Ֆ�S�,jkQ�b�����5]�]��V�C0�`zH�y���b�a ��`uQͫ�q0�����MZ�O�<�T>��P*UW�B���
´�'mD��
�ցW�������8i��I]_�Ӽ�a�eT�^�J=3�J��7�U��4���&#bZk����[ފ.���=/�ad������ f��u5��P[WׯH�<�����u�&q>|0��
�R���`-긔�[�N��.�@+��+jr��h�Ap�_e�D8�(L�a�ց�L��m�u�q�`Tp�^�����!�_�����a=�v����4���4uu�
qP<���N'��ŶV���I����_��S��O'L��wZ��>LQ�t�}��o�쌞�WW�W���4߇����&X�Ac0r����T_�y��ĺ���-�>T՗{X�Y��>T��k�n�;[������Խ����|U��ֵfܖ$����^V�t �S�`<�:�J���ԦFB�3��G��~BE�y:�g>%vd'����U��e���e��uT�t��eU�s�W�׵����:�2��V��
���2Lt~@ 3z�A��/׿[|��������_��q���( �T�ʠ�>e ���:p��e��U�P�N4�$"k�.�L��L{��GA;e�����̔�u��lq+
�욶�o��M]ݰ V����՝L����uXi�7xPs]���?I`{wvs���h����M��9F�:�t���>�g��u 38��}U>�����U��U:���d���'mG7 �����2A���;n�[]���r��h��woĪS�ӬH���wr5�Ӏ�o0P�Ի���M����CnܽR��yw�f�vBu��t�|� ��O�˹�w��5��XM[�@��Z����:\�ص��E��L�����Z�~�D�㠬s�t�|����n^�-��j�]�n���fe⾨�j�zg���P��c� �vKµW�Z ���p�wQϧ<��CX	��#Z�M̲)� ����D}��Fm�e�픏�HI	W[R���]�h5�j�&:������*j+�~'3���gP/��t��J�엢Er�L��0�����T:0� ��. �ԵH�� ;g�y9�0p�I�g���&�\#C3Xo���%a_��AC��2��j.<Ơ�Q;��$���!�=i;RT}�M�,��
+�"���Ѣ��*]�R�/L���g촣x�����ma�DܭT�0�� �Aye���io�G�>|ғY���o��&{��
��~c�k$9N���ti*�=�pD��ŝA[�ݭ�J�l�nK�ݼ�Z�0�M1]�q��~tZ�H2�����2��w	���Y_��7�m�ھn��7��-���(����MfP|�y����u�<���чw��ì=�@ἹY�-���Օ���o�^ }ε.������䂓��A��k����I�#E틳����\GM���ӵ���r%���1��򶪼٧�W�Evk*��ʣ���氧;]y?�<���������a&T��z�88Z����������:|�����6�t�+��]�Ӯ���/��.5����������Қ�ZS?�\����|���h$_�$�Raʀ�;k�I���ˏhS��K:�0�����:qz�0=�m��N&E�s�����p_��*��Jv@���T+�Z���-m�A���� ��y`M6��j��4d�tpb�`:c�����~��d����Oֿ_����Ü�k�10��T#�ݟ��0.�B�
�%8b ��HX��=x&�׹@��g#���'��x�#�^M� �z0֥�PM�M��c#q1���P�+������5��΋�R�{�e�6�5�����g��׬b/p���eOQ��D�	�p�l�̀�	�|���s��QF-�t[��(�DW�{�]-n$0�(B���Z܊E�{oc^ęx3�㈦���`sڹ6X�EC-�d9�a���
��\�8]�\��h2��a�
8Fo��6��J@����v�kB���9 ��ěI'#Z�O���z��>ZN�[nM��b�:���b�r��Y�5�%�����.��HT+�zP�f�uc�~�|���z�/��r+���ZbA�&����� @���V�}&�̀ĭ�4��X���/�~��GY�-��OD�d��ȵ}a�I�{c0%f���œ��.�ڢy�	�
�f��k�Zbx�C�S$��>|���w/����ڊ	�^	*ջe�vbm
%R�N:b|�_?~�7�ޭSm�$�g������X��֐\�߉��~���\M��6)�35ɪ��O/q��_�d��j���	��=���%�X��*�qh�$����Xc����]!7�-�?��/�V������Ĕ<�0O[�xrxAy��$�[�9`������򸎽��&3�	�%/���盽_=��j�0�ڦ()L�1Oe��uYr1%����R�p���<^4`p)J����ͼV޽�@�t唏q�P� �MP�h�H�OK���l��f�DZ{׫�V�:������6,/�i9E� w;��r �H�Ҿ���%��T��r&���O�|����R&��mÙZPK������w�l�G��k ���B ��*U�.� ��Z
���j��@�:@��u��2 � ��l2�Q�2.� ��h�N[4cr��3�]�a�h!�]��lR�-���m�YHkסuڜ��E8��j�p��wHm��8�-��pz���ҾCi�^�;�6�p�O	��Q7���SO�1(���"{������]~���������d��'�CLJ��+�\�d��#5�9���7�KQ�i igT���H1
Cht`�b�	._���)�����-c4*����Ҩ��-�Ѩ&��{�Z�(
��=��Ce��˳�< )���ѝl�	*�)M ��,�;�u.m�Ҡ:�9Y.Þº,<�����@_���	��_�r�I:"Q�Z��<���9���������{�q��#Ll���6��(Bu^�@��T֒���[���q%gA�.�L�Ck�Iiʥ'#�uJ�\�ҾS�9�]XU�.��&�M�6��,��&�-ǔ$�Ի0��v�t�wLV��eA|t���ͥ��V�o)��M�4���KC������4:��T������M:}ir_j(JS�/M���Jk����Kc��<��t�/�K�Ce�P�/7��ޡ^_�\�;��K��Tv%u�rS��I�������ʞ�NOZ̥˞�NO��Wv��t��1Tv��t�4��;i9�6p�(��JkRymO���[�����?�s������كӷ~'�Y~p���'����o<yxq��#�7#�;O�q������?�������O�����O��N���g�?�/
u;\ڪk�J���C�|T��F�K��Ҷ7���l&*:#Z6���Y����*�:#{+�'"�[�oI3�닋�B�3�FkO�^����H�"�N�.��[!��9-�Q'o���Y)�rN���4�n� w��8.��?Y�|�����֟rRn�ʍ��G�.��]<*vL�;T�� �  �q�g��l�{�P��v�RY�mqz|���\�mpL�d.�����ԣ�O�v��!e�4ƀ��B�@�n����F�u=$ ޹R��>�я�ۉ926bu�ub�ݹE�Y�G��"�T�aܥ�~\ț���51�ah��ٌ-Dp�!9��9J�=Eʛx�"�ɭٌ"-"/�Q�6.�f�iqNd���i]�(Ӣ�Ȑ��1��L-gk�IĴ�q��PnMgi�D�"0~=��B���S�X�����ÎM k����f/.XHu8���]&7btX�m����&w�py�1�v �ʈ�#�O�R����G�N��Nqz��tπ�8mF�ʯm�Q��t�R���]39�����tg�)Ng�Ra������S�6��8�wʎ8m.���b4흲G��s���Ͼ�gT:��-��o�y��;�fT�z�����؜q̲M�=:�����s���hṍ���m��:��3�l��4�|P ��-�gi��I�X�A���-��A%��v�C�C�"��bg�Gq�O����N�XsG��@����X�f�TMt�:�!��v�D���&5�1N2x�Wx�����C0�_��)�=$��i������yKo�ȭ�{p�GP[cy����
�2oQ�k�J+�y��Z�>L��_y���?�ݛE�kV���n�+<bs��_�N���_�Z>ސ]�G��{M�yZ�K��҆��� �ۭ��$_$妆V�>�lӶ��hv�%����}ٶd=�eIH���������7��(�ܑQ0���{��5|�_��67ˑ�=��o^Q y���2h缽�JTE7ИwA���y��f�v��S���ٵ�Ɣ_Ӗ�}�tXB>3�����r�!l���z�|(���U0�%06�P�xUP��Hl��x�*�C�����a�w���j��|睧o�w���|�#c�X��#Qz0.���#M�#��֦gZ��#��#��1���|U�8zLz`%��U{y��E/�*L��Ѥ�R�ܤ󦖏妙��Lwv���7�|����X��}�cV*�%!&�%p��ǹ��\�Z?m�V���u��x.u����[�zE�حMo���,9ol��N���/u2�P 6�#VY<�8�taU�L���i0�`����o�?~��i�#]�~��S����ڨ�sn�U�oT�6����Q�zs���k�*WA��`Q1��1���*�`W��\�]���Hqm��C�],V1}��}7��[ĵ���Ka �%��6�N�-V����`�mW2��t�,��6j�f��7t#Pm�2�s�d�l�js��|�h�Y`|F��><>�H`Spjh&*���#>	 �ZLf�,	�,�O��.^��3���AeZ4�P�[�-��H����'�"�H�,	�L�e�TFq�M1�"��A��i˵8$r�?{�Ö�q�]Qߒ�P&��QG�,n��JF��Q����#E�E��~P?
m}�s��q�ʅ9#<��AeWH�i�4q��OG��G������>��`��3��=���9g������^�{n`��q��W��:lc�����al���
��b،Q��<W�|��:8��g!Qag���
���X�)��U��A�1v��~������cԃ#a`L@�k�L�L��ѩx)6�qS��KK?����lP���0?r<T:j�g��Ȧ�E1m�1+_��ZI�|	���iS�Z��8�J�?�Zy�+O�$5�?z�WA�vL��p*%Q?j�u���d��J�1+ϵ�F\06&#��R^��&��Pi�ۻC�G��;��=,U�����rM&o���v�0�b��[E�Ǌ9�}m�v��l�����ނ	�W�3��|���[^�z����4��ᵪ'_��6�c��V��+�o��c���'_9���5��`�n�z���H6H�ؽ��s�[����7��+OJ�M����RbˇEw�Lj�������ڏo�����i��]tu�f��nBZ)��7[$�b�w�,�����4��U����)�Lò���L��b���y��V�U��3޷@���@��kTb�+G�Ǳ�����0Q�+��.A-˔���nA�Ҳ��Z�$D��+����b� �v�#."��-HzS�e�-[�.����� qZ�Zc��dR+-q�Ӂ�j�F[|��)K�7k�q6:y��dfw*�-�_�{��/߿K1g�I��#r���؊3����˓ܲ�x�3���l~�b��H3��W�J�:�I�֘�8����0��1I(�����f�$!�	iو�43&	�jJ��,1���5���yD��z$A�ch	@�ʌ�z�i+�X��&�1�/�o{�j�&$�&:��fx�T�7#Q�����H5�H����R
	X��{�5�g@G����8-�&�h��53��@}k]�9YC	i�o�;��.�����c�7y�-d�n�[r�d����mv�H٭��|6i!��M�i!�����<v�e��/�2����6�����ܦ���7�~R��Rsfm!�9.yi2�B�s��[���ǃM�Kg׈���i!�M��ai���wsf)�M�ˣDp�|�Ѧ�V\I4�9Jx�6OS�+	�$\	���5op���k���(��������k���T7n��t|���X#˜���/�tK�C��m&�X���j�u��8�A�Iz�؊5��G�k6I�>E���|.�!��a�[i�!�Ǵ��ס�h��u��)׍���$�.!-��q
H��uX�٦���D�B�U"�b��s#VH�HK[�Cg��KHK[���-���1�e�~�)��Q|3X���*�ǷH[ܷ9n�J+��,pR��%���m�[�v�4~�ֈo��*�(��{5J��%J�q�Qڼ.QZ�V���U��~3q���s���uY��,Q�y|�o]Vm�(�[�U��&�n3;k�����b�o]V=�nQ��n��[���u{�ݢ,i�w��fI�v��=i���_�t�[�,h���"��b����!��,�H0G"=X�R�C[��8\��f�HrhXFð��?Z�nT�סoVa��+r)��T�/w�H��OK��!F���ڎc^�eo��Ċ�$	&�K����d[ko�ȋ��4?��n�=P�>x������V��C�w������~-%\ȡ�����hY��7U�q�n��4� A��'ٙl:���?/t��˟���t��0¯Sql|����jty5>�	�u�/噄������g�?��q��֟��}.%B������<�j!I�_�ZeN�>��M��;���\MO��G���_��/����ȯ�#�wwx�GbO��Q{V�����k?�p��$<�=�;l���c��1y�V��B~�sd�4zB��LI޲�˔űS��`�eq��ǋ5*,���0�4#j�f�Y卡c־0��T)I84���,�6��1r�>x�a��>�	*���?�������΍(�Fђ���M��i����\�0||;���F.�*�,/�N����?y��.��C ZK�{0g�J�������/����	�y����Y�4�'b8^H{���g<��s�'�?���'��bA���s���.�m��U�����7/҅�/���7��&Fnê1*(�(K���g���Q����zlPQ`�y���:��հn�NX*����+bT��!�%���EW��26��D��K2���x=�U�=����1b��G1����pݣ���)���ʱ�{�_^{���/k�      #   �   x�U�K
A�ur���<��0�6`H2��m�u�zT% ݓdx���u�h�T�$fR2�V�Z���5LƊK�6��<��gm�O�H�Ú���s�����X/]��}i�+��(�ڇ�;S�0���m��o��M�      !   �  x����n�0���)�_5����3�#�d��RK�['T�>��	�-+P���3����fp�0|u��0Ƹ���6� ^�|�V2(3Ŕf�&�������
�]�
����7ߗh�x,�k	��=���e���gh����a���ad�W��2������ƼU�h��ߓY<G&"K��5�&>1���c�,Q��[.�΅��}��Mm?M�#��!J �4
5��u���j�o)��)z���/IN�+��B�������C��Sg�je蹸P�D�������wM[�H�4)~�gq��a+�C�4}BL����/a�$&�z��w6�<��I�y�J1�:����3��S�$F�ؚ�(ܜ:rș.��_�@�أs��O��f��|x��<�J��f�6�;���QAe\ �����������^�P%�L��")�(��wq/S䣌�6m��8����9�����w\�9ɣEr!0i�XD<ZdB �8�\��Q ��Q'�C�`_+� �ɒ�Y��7:���� g�y=E_,2��c=.�/gĜ�8���La�|A���"�L��"�~:"�����t� �t��[�R��5��nl�2B�l�	�ND(���?�|���U�v��M�Q�,Qe�Ř�@�Л�&� �2�\R�fz=�:��� ��)�,
�^������'��X�������E��ϵ8'��<���M�ïl���?�~�      2   5  x���Ǫ2k� �q��y�|9���9+R9�\W\�3ؿ}� �<���Ө4�ʕa�Z�Qw1Nt�ܭ���W�\6o<���`}0{�������?@w�ݯ�?��?%��l�+$���8�&Zt?��u��`��u�ϕm&2˸��t=��X��`�\̝KE�͎��h���<�li���m��0�ml��ඟ7{2lƃh��m590�?~W`L��A����lo�4ַ><��t�٬�'q]�dz]���B ��=��B�h3!	��yÄ�	rjCb�)Q��0�R"_��'E�9>%냜C�|�P!�1e<�f�N�N.��%B�)AP���N��V�n%[��-�&�S��b��D�HY�b>�?��:���h��t��<���^׮v��q@>��BI�A���%rTV /k��a��T�I�^ʆ!��$2K%Ֆ{s v�.��#Kpc�yš�:�'�s��N�yR�������>�RH�K���fb���"�6o�4%�
�K-�*�u~Z�7uW-x=-�]�^.v�
�����c4��\|F
F}� ���(q]+� V�'	�8O�EĐ��8��wEL���4�w����Փ�q/�c��8ޯ+[������'�T��!9y�"�8 Z�H/J�:%ciqɺ:����D����J $w-Η�qe�G��7�����{�h 5آ?;ګ�A��>"�H�K��̄i�@��nhM�fѰ����D�C�'��9�<
��]w�kx�k=.ǣ;�`�޽�>������Bp�1�雈��ô��t/o��W<�m���4�W�H�<�F�fx(�጖��A����f:Z�������p޻D�����E�R(Ȼ\C��v�Ky�G�G	�yS�tx���IDC��gj�t=��=3_��ڪo���.��a�+�1[�ΟDBA�/!��]�[�)⎄u�b��f�X�r�E�~g��X��L̻כ�q٭n79:	<N4c=�򙼳��e�?�R(�.^c�/iR˵�i�wO;/HL7��Z �ֳ�$N����
��1'��)����z�z�?�m�Q;�Qe:��ID~�(E�(p�Z0�s3�����>� 2��v+��Dc���c�Hب�������s����H�Cw��WJ�p�'U(�s����5��&�w�	lH��[9@j���e�0�R�����l����Er�NV�6����:���8��Q����؋O"�����!��"��e���F�[�w��¦l�wn��y���R��һ1p��	%2Y5�}�Lo0���8F�]{^a�E �Q�X����:��?�-13'6��}%�e�W��a��Kz���Lg���h7�$���N�ɍ#4Y�A$B^�l�B�w��,
.K�/�ض	�Q����P�.�Q񝵕=�B����۔�}��w��lk`��8��k�[l�!� ������h�D�NnT(�̜uuNXyN�� ��It�A�ٖ�Av�:����V��U�Ƕx�a�J��b��� �T!�� {��_"���m�U��a����-�L�Q�a~�1�:L�IAg������=[Z�vW���}4��H����i�����ދ��r��i
,��5X�Q�U'tPn��u�PԪ���f�\���w�S���9�����������D#��#�{�h�s-�%���u�Ό%=�
�i���h*�LaY�Q|�֜�D�U��a���4�t;�ۘ��?�^�#�3,}O׺�ꥅʠ���<��B/�����;;�u�U�B��i�Q�h��C�D��=[�--�=�N7 4���H(��ꈘ|ע4k��� qRU�l��uT�с��N�������������Ӛ���>�ϓb��jV���[8�Դ?�(P �3Ƞx'Z�_U�*w9'Y�1�Ԁ��S]I��D��`ŵj��m��LN��y���������oY��Q�g���,S0�c�x'�$�����-$s��W$���H�8�N�t���x|:�ře|z,�|[�6Ҿ��5/�?w���}��/ �FV�~�q�S�b�P��?R3_����|<&'����i2��O�Yv���g�\F�^e�i}`�����`���
��0Y�Ɠ�+�r�|�A�.D�Y�nl�L�l�jtx[��tTR(��A���h���0�@H�xuD���>@�}/�ZfU��W�l���baa@#KQ�D�w�D����=�l6W�y6'�W�x���n�.wT�D����g���~N��K��5��a��j����wn��(���]�h��g3,�5�i�'po�gL
[���һ�D�� B
z�"  ���l*#�Et5��,ҭ:�@����I�����>�x����v>�<��������7V�� ��]o��6����~;��M�6�K��03�6�68�3�
i&�;;�}J�Yv�������d̍i�&�}D�����'�8���|	���#�����*[*8j�"��FMI�.�i�E��B�G��6�u.naM{����M�f���ғ��O��Z�O��h���wnTЫ������r3Y#&*f��A�l7R뜷�t�wYeS�x5�jc���a[W�C���S�H ��ӓ��S�$���"�%~�Y����5Fٹ�˙
��%ɉGp�E��ԃL�����,����z��Z�qf�6r�\��%?����*��D
�ɨ����=e�p�ɳ$6��h��Zf�F�,��:�J�`��7��?��鴛mvs|��sp:��|���ήng����`�x�7y�|��RVY��D�2y	%V����D�e�\�?��cu�K���'7��2_�M�o�'U��K� x��������
�:�           x��Y�n�}~E��9+���� ��8�c � ��S�1�=�$�����	Y��@�F#��~���%�[Uus���1�%r��n�{ιK�6;���z���.��B���Au\?��N�$i��z����a��2󼜩y���f�P��(�E��j\�\���qW��D%:V����\͢2�{��4�C&��rZd&6:���)��xpn�c���\Ϻ��e����G�)�4PQ�
>��8���8���q�U?M�e�B�~�i2)u��fRN#9�b�[u�I�Qj�@M�hό#����ʸH3��C�kBCa�yd���ɟ��Ҽ� {���{�g��Y
�F�0ne��ux\��Gs���2����hV�o=����Ȭ�����m���7-I9�Fj��O�lV@�
���c�%�*ᇐ+LI9�E��!��k����΄�4��,�H����U`T�J�ԅ��vK`�:Cw��
#�V�#�����̢S���<1�E�=��4�4i�.���Ek+j�C������t�i����tl����"*���E����ݮ�P�J�� v}@#��y��+�q�Cѳ�h?�. �ֱN������XM�\J|��X�r�ӋG�tNY�P� ���fb�r?�U2���c�L6s ?��f(��=y41T��Bq�ڐ��qd�h����.����9*�sҁxg\�L<��Wx��W^u�2 ]u��_w[
o�Y���F�G�)�XN=	DJ6�dg�Ap#A��=��/l��NT$����B�Ű�J��Ʌ�!�ޖ1N�Y���Ph��jZL[(�����-��]��O��f��Ɔ��u���|�Y�KXL���K��\i���C��'Q�S���f�Xy}���UMn�k��ت�Y$�#�/��@1�!w]��Z���p�n��`�F�$V!�� s�"�}9F�3�Ѷ�_��%�f��s}��'�q� (�*y�V��3JA�6�T_�a�f�S@�#.%p�RH]��p�vw{ZIM �t��0o� �J����4���`�Y�ț�J�x��l�J��<sDoW�A�|�'qH�C;�����F��H�u
�L,���ʈ��6j�����5+���?c#�1���(B.,V�t���7�O�������	ɝ�0¨��L^JWpm�\��X�9�|�$�����j����{Ú����xݲ��I��O}�2D�x@ �b������y�z0�6?�*p�41��C��	'"V/��Ҽe�k��؄sEJ�D%����ϕ?�@��]_�Q�����d���5��F�s[fg�Ӑ�j|��%?��k��eO���0j�^�N��b�s�Y�8z��q`;ht�m����Gi;s\���F7�t!^�kN�T���HY��E�h �������ŢCV�Rfɺ �>!�<P��������1=M�	3��]������I���rMR�G])GT�G�n�'9$��i�� ��-1L(�'T�$�m���\���h(���B9i]��Kb�sח����l	Ģ#�`����=�
%{�`KU�˘�{<^pb�I�Ung>$13��F��e����
��1��H���&hؗ���乭D�X�
���L4,�v/-�	x+�D�ց�̙ć�������~�3��.������;��nQ��כgQ\�&��Q2�_v��M'if��Y��������Z��=z�}��E���c�QTĻ?����N��p|g���W����u}P]WW�k��:V���>����v8��������E�a8��7z�AO�l��g:���!Q��x�p��|�'ܷ��Xn��F��׷~����j]���~�o-o���˃��e�=T�-���_��T�CDO���>�s�|�'&��&$<���Y��>����T���D~��E�P�|��A����Z�/��� Tp	�X�C��auR���ok�c�~�U�9\��7�!�y&��kU�����O�ኣ�>S�+0����.�/��e��e/��}����-��a�(~5g��S|������/�K_ᕪz���Yܼ�nF�s~�@����.ڮ�����׫�C���c����VN/���ǈ����tsQ�6Wt�����X�4x��z>�7���k�W�^ST�p�i��N�D�� 1�f�Qq���bE�P�Q�p��Df1�IX�X��<�K/:���vЩ�j�}m-�u����í�t��t�c���~�ar�����;O��W��7Ru�W�Q�e`���5�C�	G��|���7��~g��2X�T��P�`�"}\@\D�G�L 8Gv�I��Gu`���!�L���UrU�R1#a���`(E�ߴ�٥�3�uFw	��|�޽������e��"�f�b1��U#��r	T�x�m�@��+���Y���휌<�B��]W�S
;&�yx��q���t��~N~�$+��	^�ҳ�vF���8<��J�W���L�����wd���ngԩ�E2��w��5�?֕K��W�.����Lkr�o�� ����+������r���;�8n�A&R��Jι���O��?O[D#)�rP$/a���}M��%�R�$��Z��A� S����鹦�����k_�kV��*�F0��f&K���<.{�D�#�%��1_�
� ��!��%��W��)6O.��Bν����0.l�|�R���D����z�s����隴7���K��&�y���f8tG[����RQ۰E���!@0�4��f�������3�l�t���/���<讬��t��             x�3�4�4�2�4�4�24�4�4����� &'�      :      x�34�446�4�242�As(#F��� N��         *   x�3�4�4�2��4����\����F�f`ژӜ+F��� f{      6      x������ � �         �   x�}�Aj�0E��=�k5#�u�B)β�dY(J"\�X2�@OQz��M�#�V 1�y33��l�ZT��#��� (8�9������[�q-��}Od�e�U�&�(%`�o�5_��֪v��l�I�ҴSi���4��Ň'�k�+9r���"/E��x�>��:Meb���n��)�)R�;�o�O<�C<]_^⾇���:6�
��Rb9;�Q�q)�.���Ƴ,���p�         	  x������@��3Oa�0$�d�.]�}�!�8�xY��b��d�E�e� ���g8y#��n	�b8�s����ыA2�*�ZG<6^�t}��H������ ����#��;���Y����9�z�c�4�"KjV�r:H�tg�RZ���7}����mm���p���dɧ�?���e���@G볻�a�}�S�T��}3������H��(��S��pk�K�6��Ψ����R���C�&��r\����li��o̮*�y��:�1v���            x������ � �         �   x��Ͻ�0�}[�	~lNw7�b
B�^��>���o$��].���/���} @���Q���,Kb�9ʌj;і"��(�<ƨ�Ӧ��9H���#�@;^pm!v`������%����S"ab��~!�Z#�ʔ��^_�g}�o����T0|4����$Qac��:-³�ǻ~<� ���h�1~����         w   x�346�443�/칰�bÅ��]ؤpaʅ@� ���ǙXPP�_���i�ehl�ihn �t�f�&�@u�17c�2�s :���,��י�� �3.l)�j����� C5q'      7   G   x�-���@D�3cDXF{��:�9����E�E�3x���Ɖ��������1��/LW���k�����N�     