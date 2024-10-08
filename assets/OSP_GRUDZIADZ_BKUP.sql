PGDMP  4                    |           OSP_GRUDZIADZ    16.2    16.2 #               0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            	           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            
           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    16609    OSP_GRUDZIADZ    DATABASE     �   CREATE DATABASE "OSP_GRUDZIADZ" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Polish_Poland.1250';
    DROP DATABASE "OSP_GRUDZIADZ";
                postgres    false            �            1259    16622 
   czlonkowie    TABLE     h  CREATE TABLE public.czlonkowie (
    czlonek_id integer NOT NULL,
    name character varying(50) NOT NULL,
    surname character varying(80) NOT NULL,
    birth date NOT NULL,
    sex character varying(11) NOT NULL,
    pesel character(12) NOT NULL,
    rank character varying(90) NOT NULL,
    is_commander boolean NOT NULL,
    is_driver boolean NOT NULL
);
    DROP TABLE public.czlonkowie;
       public         heap    postgres    false            �            1259    16621    czlonkowie_czlonek_id_seq    SEQUENCE     �   CREATE SEQUENCE public.czlonkowie_czlonek_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public.czlonkowie_czlonek_id_seq;
       public          postgres    false    218                       0    0    czlonkowie_czlonek_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public.czlonkowie_czlonek_id_seq OWNED BY public.czlonkowie.czlonek_id;
          public          postgres    false    217            �            1259    16611    users    TABLE     �   CREATE TABLE public.users (
    user_id integer NOT NULL,
    login character varying(100) NOT NULL,
    username character varying(100) NOT NULL,
    password character varying(255) NOT NULL,
    permissions character varying(20) NOT NULL
);
    DROP TABLE public.users;
       public         heap    postgres    false            �            1259    16610    users_user_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.users_user_id_seq;
       public          postgres    false    216                       0    0    users_user_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;
          public          postgres    false    215            �            1259    16631    wyjazdy    TABLE     e  CREATE TABLE public.wyjazdy (
    wyjazd_id integer NOT NULL,
    title character varying(255) NOT NULL,
    day date NOT NULL,
    number character varying(100) NOT NULL,
    type character varying(50) NOT NULL,
    adress character varying(150) NOT NULL,
    commander integer NOT NULL,
    driver integer NOT NULL,
    ratownik1 integer NOT NULL,
    ratownik2 integer NOT NULL,
    ratownik3 integer,
    ratownik4 integer,
    takeoff time without time zone NOT NULL,
    arrival time without time zone NOT NULL,
    departure time without time zone NOT NULL,
    comeback time without time zone NOT NULL
);
    DROP TABLE public.wyjazdy;
       public         heap    postgres    false            �            1259    16630    wyjazdy_wyjazd_id_seq    SEQUENCE     �   CREATE SEQUENCE public.wyjazdy_wyjazd_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.wyjazdy_wyjazd_id_seq;
       public          postgres    false    220                       0    0    wyjazdy_wyjazd_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.wyjazdy_wyjazd_id_seq OWNED BY public.wyjazdy.wyjazd_id;
          public          postgres    false    219            [           2604    16625    czlonkowie czlonek_id    DEFAULT     ~   ALTER TABLE ONLY public.czlonkowie ALTER COLUMN czlonek_id SET DEFAULT nextval('public.czlonkowie_czlonek_id_seq'::regclass);
 D   ALTER TABLE public.czlonkowie ALTER COLUMN czlonek_id DROP DEFAULT;
       public          postgres    false    217    218    218            Z           2604    16614    users user_id    DEFAULT     n   ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);
 <   ALTER TABLE public.users ALTER COLUMN user_id DROP DEFAULT;
       public          postgres    false    215    216    216            \           2604    16634    wyjazdy wyjazd_id    DEFAULT     v   ALTER TABLE ONLY public.wyjazdy ALTER COLUMN wyjazd_id SET DEFAULT nextval('public.wyjazdy_wyjazd_id_seq'::regclass);
 @   ALTER TABLE public.wyjazdy ALTER COLUMN wyjazd_id DROP DEFAULT;
       public          postgres    false    220    219    220                      0    16622 
   czlonkowie 
   TABLE DATA                 public          postgres    false    218   �+                 0    16611    users 
   TABLE DATA                 public          postgres    false    216   -                 0    16631    wyjazdy 
   TABLE DATA                 public          postgres    false    220   �-                  0    0    czlonkowie_czlonek_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.czlonkowie_czlonek_id_seq', 6, true);
          public          postgres    false    217                       0    0    users_user_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.users_user_id_seq', 2, true);
          public          postgres    false    215                       0    0    wyjazdy_wyjazd_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.wyjazdy_wyjazd_id_seq', 2, true);
          public          postgres    false    219            d           2606    16629    czlonkowie czlonkowie_pesel_key 
   CONSTRAINT     [   ALTER TABLE ONLY public.czlonkowie
    ADD CONSTRAINT czlonkowie_pesel_key UNIQUE (pesel);
 I   ALTER TABLE ONLY public.czlonkowie DROP CONSTRAINT czlonkowie_pesel_key;
       public            postgres    false    218            f           2606    16627    czlonkowie czlonkowie_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.czlonkowie
    ADD CONSTRAINT czlonkowie_pkey PRIMARY KEY (czlonek_id);
 D   ALTER TABLE ONLY public.czlonkowie DROP CONSTRAINT czlonkowie_pkey;
       public            postgres    false    218            ^           2606    16618    users users_login_key 
   CONSTRAINT     Q   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_login_key UNIQUE (login);
 ?   ALTER TABLE ONLY public.users DROP CONSTRAINT users_login_key;
       public            postgres    false    216            `           2606    16616    users users_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    216            b           2606    16620    users users_username_key 
   CONSTRAINT     W   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);
 B   ALTER TABLE ONLY public.users DROP CONSTRAINT users_username_key;
       public            postgres    false    216            h           2606    16640    wyjazdy wyjazdy_number_key 
   CONSTRAINT     W   ALTER TABLE ONLY public.wyjazdy
    ADD CONSTRAINT wyjazdy_number_key UNIQUE (number);
 D   ALTER TABLE ONLY public.wyjazdy DROP CONSTRAINT wyjazdy_number_key;
       public            postgres    false    220            j           2606    16638    wyjazdy wyjazdy_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public.wyjazdy
    ADD CONSTRAINT wyjazdy_pkey PRIMARY KEY (wyjazd_id);
 >   ALTER TABLE ONLY public.wyjazdy DROP CONSTRAINT wyjazdy_pkey;
       public            postgres    false    220            k           2606    16641    wyjazdy wyjazdy_commander_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.wyjazdy
    ADD CONSTRAINT wyjazdy_commander_fkey FOREIGN KEY (commander) REFERENCES public.czlonkowie(czlonek_id) ON UPDATE CASCADE ON DELETE RESTRICT;
 H   ALTER TABLE ONLY public.wyjazdy DROP CONSTRAINT wyjazdy_commander_fkey;
       public          postgres    false    220    4710    218            l           2606    16646    wyjazdy wyjazdy_driver_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.wyjazdy
    ADD CONSTRAINT wyjazdy_driver_fkey FOREIGN KEY (driver) REFERENCES public.czlonkowie(czlonek_id) ON UPDATE CASCADE ON DELETE RESTRICT;
 E   ALTER TABLE ONLY public.wyjazdy DROP CONSTRAINT wyjazdy_driver_fkey;
       public          postgres    false    4710    218    220            m           2606    16651    wyjazdy wyjazdy_ratownik1_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.wyjazdy
    ADD CONSTRAINT wyjazdy_ratownik1_fkey FOREIGN KEY (ratownik1) REFERENCES public.czlonkowie(czlonek_id) ON UPDATE CASCADE ON DELETE RESTRICT;
 H   ALTER TABLE ONLY public.wyjazdy DROP CONSTRAINT wyjazdy_ratownik1_fkey;
       public          postgres    false    4710    220    218            n           2606    16656    wyjazdy wyjazdy_ratownik2_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.wyjazdy
    ADD CONSTRAINT wyjazdy_ratownik2_fkey FOREIGN KEY (ratownik2) REFERENCES public.czlonkowie(czlonek_id) ON UPDATE CASCADE ON DELETE RESTRICT;
 H   ALTER TABLE ONLY public.wyjazdy DROP CONSTRAINT wyjazdy_ratownik2_fkey;
       public          postgres    false    220    4710    218            o           2606    16661    wyjazdy wyjazdy_ratownik3_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.wyjazdy
    ADD CONSTRAINT wyjazdy_ratownik3_fkey FOREIGN KEY (ratownik3) REFERENCES public.czlonkowie(czlonek_id) ON UPDATE CASCADE ON DELETE RESTRICT;
 H   ALTER TABLE ONLY public.wyjazdy DROP CONSTRAINT wyjazdy_ratownik3_fkey;
       public          postgres    false    220    218    4710            p           2606    16666    wyjazdy wyjazdy_ratownik4_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.wyjazdy
    ADD CONSTRAINT wyjazdy_ratownik4_fkey FOREIGN KEY (ratownik4) REFERENCES public.czlonkowie(czlonek_id) ON UPDATE CASCADE ON DELETE RESTRICT;
 H   ALTER TABLE ONLY public.wyjazdy DROP CONSTRAINT wyjazdy_ratownik4_fkey;
       public          postgres    false    4710    218    220               n  x�͔OO�0��|�ހd3m��œQ�P/�l5�m-�:�~zہ�̃��K�g�<�<���,?,�d���m�*Xz��B�\��F�|�2pRRT�<��jm<}w��V�p�$<w ���(K�3*�I�F�<]�>�0@�ϫ�Ⱦ�M)��
C��ط��T�5'�@߃؇����DY�=H�$����+)*z����IX��
.Iv�e�`��Q�a��hC�p]r�"5�����`7D���?�P���,n�E!�Q|Z�YQJ�]��&�=Qr�n��Sib.vf$��"׃ͫX1��S��g�AY�nK
>�l��m��-;4�	����}~�갨��yf�͢H
Q�dE{�E���> "ˍ�         �   x����
�0E���ٵ�Phԕ]tQ����h��id,�_o�~����\N��nm���O�/�D*�P2�-��V������U0H��R	����P�rGZu_9^�1�EO7��O!B�'Ҡ��e��_��}��Ie*�tp�u^uU�'�|6_$N��(�ޠ�^         3  x�Ց�N�0����-a�j��b�����xck��BK
H��=�T�LH����=�ȷ�������(���q���D�jK��!�U�t�5E(�l������!���o�����لl�����t�>G���Y�k;'C�,��|s���Ü*���A�d3j4
������h/K��2Y/S�W)K�>��Oy��Rm{�4�55�p4�c��/v�$�DgN3�8��z��O����e�4J� !ص������<���f0�2�(��x�a�}���Q0ȃM��?F6���|b�+g�K�l�	z��     